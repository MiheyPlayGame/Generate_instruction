# Generate_instruction
Task GenAI-2-39 for NSU "Project Introduction" course

## Task description
Generate detailed step-by-step instructions with substeps from user questions using AI models.

## Guideline (Original Task Requirements)
1. Get the prompt
2. Generate.
3. Check the structure.
4. Output.

## Features
- **AI-Powered Generation**: Uses Ollama for instruction generation
- **Quality Validation**: Automatically validates instruction quality and regenerates if needed
- **Structure Analysis**: Analyzes instruction structure with step and substep counting
- **Interactive Interface**: User-friendly command-line interface for question input
- **Error Handling**: Comprehensive validation and error handling

## Functions

### `generate_instruction_prompt(prompt: str, add_substeps: bool = True) -> str`
Generates a formatted prompt for instruction generation.

**Parameters:**
- `prompt` (str): The original question or prompt to convert to an instruction
- `add_substeps` (bool): Whether to include substeps in the instruction format (default: True)

**Returns:**
- `str`: Formatted prompt string ready for AI model processing

**Raises:**
- `ValueError`: If prompt is empty or invalid


### `get_instruction_stats(instruction: str) -> tuple[int, list[int]]`
Analyzes instruction structure and returns statistics about steps and substeps.

**Parameters:**
- `instruction` (str): The instruction text to analyze

**Returns:**
- `tuple[int, list[int]]`: Number of main steps and list of substeps per step

**Raises:**
- `ValueError`: If instruction is empty or invalid


### `main()`
Demonstrates the instruction generation functionality with user interaction.

**Features:**
- Interactive question input with validation
- Quality control with automatic regeneration
- Detailed statistics about generated instructions
- Comprehensive error handling and user feedback


## Running the Demo
```bash
python generate_instruction.py
```

## Dependencies
- `requests`: For HTTP requests to Ollama API
- `sys`: For system path manipulation
- `os`: For operating system interface
- `ollama`: For local AI model support (external service)

## Installation
```bash
# Install Python dependencies
pip install requests

# Install Ollama (choose your platform)
# Windows: Download from https://ollama.com/download/windows
# macOS: brew install ollama or download from https://ollama.com/download/mac
# Linux: curl -fsSL https://ollama.ai/install.sh | sh

# Start Ollama service
ollama serve

# Pull the model (in another terminal)
ollama pull llama2
```

## Implementation Details
The implementation provides a comprehensive instruction generation system:
- Provides tips for better results (questions starting with "How", ending with "?", in English)
- Converts user questions into configurable and structured prompts for AI models
- Uses `ask_ollama` function from `using_ollama.py` module
- Dynamically imports AI backend modules from GenAI-1-39 directory
- Regenerates instructions that don't meet quality thresholds
- Counts main steps and substeps in generated instructions


## Materials
- [GenAI_1_39 module](https://github.com/FedosDan2/GenAI-1-39)
- [Ollama Documentation](https://ollama.com)
- [Requests Library](https://requests.readthedocs.io/)
- [Python sys module](https://docs.python.org/3/library/sys.html)
- [Python os module](https://docs.python.org/3/library/os.html)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
