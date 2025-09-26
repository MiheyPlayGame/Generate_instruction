# Import system modules for path manipulation
import sys
import os
# Add the GenAI-1-39 directory to the Python path for module imports
sys.path.append(os.path.join(os.path.dirname(__file__), 'GenAI-1-39'))
from using_ollama import ask_ollama


def generate_instruction_prompt(
    prompt: str,
    add_substeps: bool = True
) -> str:
    """
    Generate a formatted prompt for instruction generation.
    
    Args:
        prompt (str): The original question or prompt to convert to an instruction
        add_substeps (bool): Whether to include substeps in the instruction format
        
    Returns:
        str: Formatted prompt string ready for AI model processing.
        
    Raises:
        ValueError: If prompt is empty or invalid
    """
    
    # Validate input prompt
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    new_prompt = f"Generate a detailed instruction for the following question: {prompt}"

    # Add substep formatting instructions if requested
    if add_substeps:
        new_prompt = f"{new_prompt}\nAdd substeps to the instruction"
        new_prompt = f"{new_prompt}\nFormat your response like this:\nStep 1\n\t1.1.\n\t1.2.\n\t...\nStep 2\n\t2.1.\n\t2.2.\n\t...\n..."
    else:
        new_prompt = f"{new_prompt}\nFormat your response like this:\nStep 1\nStep 2\n..."

    return new_prompt


def get_instruction_stats(
    instruction: str
) -> tuple[int, list[int]]:
    """
    Analyze instruction structure and return statistics about steps and substeps.
    
    Args:
        instruction (str): The instruction text to analyze
        
    Returns:
        tuple[int, list[int]]: Number of main steps and list of substeps per step
        
    Raises:
        ValueError: If instruction is empty or invalid
    """
    
    # Validate input instruction
    if not instruction or not instruction.strip():
        raise ValueError("Instruction cannot be empty")
    
    # Split instruction into individual lines for analysis
    lines = instruction.split('\n')
    num_steps = 0  # Counter for main steps
    num_substeps = [0]  # List to track substeps per step (index 0 unused)

    for line in lines:
        line = line.strip()  # Remove leading/trailing whitespace
        
        if not line:
            continue
            
        if len(line) > 0:
            # Identify main steps (lines starting with "Step")
            if line.startswith('Step'):
                num_steps += 1
                num_substeps.append(0)  # Initialize substep counter for this step
            # Identify substeps (lines starting with number followed by dot)
            elif line[0].isdigit() and line[1] == '.':
                num_substeps[-1] += 1  # Increment substep count for current step
        
    return num_steps, num_substeps


def main():
    """
    Demonstrate the instruction generation functionality with user interaction.
    """
    print("=== Instruction Generation Demo ===")

    # Provide guidance for better results
    print("""Enter your question for instruction generation
    The result will be better if the question:
    - begins with \"How\",
    - ends with a question mark,
    - is in English.""")

    try:
        # Get user input with validation
        question = input().strip()
        while not question:
            print("Question cannot be empty! Enter question again: ")
            question = input().strip()

        # Generate formatted prompt for AI model
        formatted_prompt = generate_instruction_prompt(question)

        print("\n=== Prompt ===")
        print(formatted_prompt)
        print("\n=== Generation ===")
        
        # Generate instructions with quality validation
        while True:
            # Generate instruction using AI model (Ollama)
            instruction = ask_ollama(formatted_prompt)

            num_steps, num_substeps = get_instruction_stats(instruction)
            num_steps_with_enough_substeps = sum(1 for substeps in num_substeps if substeps >= 2)
            num_total_substeps = sum(num_substeps)

            # Quality check: require at least 3 steps with 2+ substeps each
            if num_steps_with_enough_substeps >= 3 and num_steps >= 3:
                break
            else:
                print("Instruction is not good enough. Generating again...")

        print("\n=== Instruction ===")
        print(instruction)
        
        print("\n=== Instruction Stats ===")
        print(f"Number of steps: {num_steps}")
        print(f"Number of steps with substeps: {num_steps_with_enough_substeps}")
        print(f"Number of total substeps: {num_total_substeps}")
        print("\n=== Demo completed successfully! ===")
        
    except Exception as e:
        print(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()