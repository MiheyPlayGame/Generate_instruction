# Generate_instruction
Task GenAI-2-39 for NSU "Project Introduction" course

## Task description
Generate detailed step-by-step instructions from user questions using AI models.

## Guideline (Original Task Requirements)
1. Get the prompt
2. Generate.
3. Check the structure.
4. Output.

## Features
- **AI-Powered Generation**: Uses Hugging Face transformers for instruction generation
- **Quality Validation**: Automatically validates instruction quality and regenerates if needed
- **Structure Analysis**: Analyzes instruction structure with step and substep counting
- **Interactive Interface**: User-friendly command-line interface for question input
- **Error Handling**: Comprehensive validation and error handling
- **Bilingual Support**: Supports both English and Russian instruction generation

## Functions

### `generate_instruction_prompt(prompt: str, add_substeps: bool = True) -> str`
Generates a formatted prompt for instruction generation.

**Parameters:**
- `prompt` (str): The original question or prompt to convert to an instruction
- `add_substeps` (bool): Whether to include substeps in the instruction format (default: True)

**Returns:**
- `str`: Formatted prompt for instruction generation

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


### `generate_instruction(prompt: str) -> str`
Generates step-by-step instructions using AI models (from GenAI_1_39 module).

**Parameters:**
- `prompt` (str): Formatted prompt for instruction generation

**Returns:**
- `str`: Generated instruction text

**Note:** This function is imported from the GenAI_1_39 module and supports both Ollama and Transformers backends.


### `main()`
Demonstrates the instruction generation functionality with user interaction.

**Features:**
- Interactive question input with validation
- Quality control with automatic regeneration
- Detailed statistics about generated instructions
- Support for both English and Russian questions
- Comprehensive error handling and user feedback


## Running the Demo
```bash
python generate_instruction.py
```

## Dependencies
- `transformers`: For Hugging Face model integration
- `torch`: For PyTorch backend support

## Installation
```bash
pip install transformers torch
```

## Implementation Details
The implementation provides a comprehensive instruction generation system:

### Main Module (`generate_instruction.py`)
- **Prompt Formatting**: Converts user questions into structured prompts for AI models
- **Quality Validation**: Ensures generated instructions meet minimum quality standards
- **Statistics Analysis**: Provides detailed analysis of instruction structure
- **Error Handling**: Comprehensive validation and user-friendly error messages

### AI Backend Modules (`GenAI_1_39/`)
- **Transformers Integration** (`using_transformers.py`): Hugging Face model support with Russian language optimization

### Key Features:
- **Automatic Quality Control**: Regenerates instructions that don't meet quality thresholds
- **Structure Analysis**: Counts main steps and substeps in generated instructions
- **Bilingual Support**: Optimized for both English and Russian instruction generation
- **Flexible AI Backends**: Easy switching between local and cloud-based AI models
- **Reproducible Results**: Configurable random seeds and temperature settings

## Materials
- [Hugging Face Transformers Documentation](https://huggingface.co/docs/transformers/)
- [PyTorch Documentation](https://pytorch.org/docs/)
- [Sberbank AI Models](https://huggingface.co/sberbank-ai)
- [Text Generation with Transformers](https://huggingface.co/docs/transformers/tasks/language_modeling)
- [GenAI_1_39 module](https://github.com/FedosDan2/GenAI-1-39)
