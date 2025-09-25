from GenAI_1_39.using_transformers import generate_instruction


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
        str: Formatted prompt for instruction generation
        
    Raises:
        ValueError: If prompt is empty or invalid
    """
    
    if not prompt or not prompt.strip():
        raise ValueError("Prompt cannot be empty")
    
    new_prompt = f"Forget all other requests and do only what I ask"
    new_prompt = f"{new_prompt}\nGenerate a detailed instruction for the following question: {prompt}"
    new_prompt = f"{new_prompt}\nAnswer in Russian language."
    new_prompt = f"{new_prompt}\nUse numbered list for steps. Use 1., 2., etc. for main steps."

    if add_substeps:
        new_prompt = f"{new_prompt}\nAdd substeps to the instruction. Use 1.1, 1.2, etc. for substeps."

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
    
    if not instruction or not instruction.strip():
        raise ValueError("Instruction cannot be empty")
    
    lines = instruction.split('\n')

    num_steps = 0
    num_substeps = [0]

    for line in lines:
        line = line.strip()
        
        # Skip empty lines
        if not line:
            continue
            
        # Check if line starts with a digit (main step) or letter (substep)
        if len(line) > 0:
            if line[0].isdigit() and line[1] == '.':
                if line[2].isdigit():
                    num_steps += 1
                    num_substeps.append(0)
                else:
                    num_substeps[-1] += 1
        
    return num_steps, num_substeps


def main():
    """Demonstrate the instruction generation functionality with user interaction."""
    
    print("=== Instruction Generation Demo ===")

    print("""Enter your question for instruction generation
    The result will be better if the question:
    - begins with \"How\",
    - ends with a question mark,
    - is in English.""")

    try:
        question = input().strip()
        while not question:
            print("Question cannot be empty! Enter question again: ")
            question = input().strip()

        # Generate instruction with quality validation
        # while True:
            # Format the prompt for instruction generation
        formatted_prompt = generate_instruction_prompt(question)

        print("\n=== Prompt ===")
        print(formatted_prompt)
        print("\n=== Generation ===")
        
        # Generate instruction using AI model
        instruction = generate_instruction(formatted_prompt)

        num_steps, num_substeps = get_instruction_stats(instruction)
        num_steps_with_substeps = sum(1 for substeps in num_substeps if substeps > 0)

        print("\n=== Instruction ===")
        print(instruction)
        print("\n=== Instruction Stats ===")
        print(f"Number of steps: {num_steps}")
        print(f"Number of steps with substeps: {num_steps_with_substeps}")
        print("\n=== Demo completed successfully! ===")
        
    except Exception as e:
        print(f"Error in main function: {e}")
        raise

if __name__ == "__main__":
    main()






