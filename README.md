# questioner
This project aims to interact with the OpenAI ChatGPT model to assist in answering a user question related to a development project. It consists of multiple Python scripts for querying, processing, and interacting with ChatGPT to gather information about the project and provide answers to user questions.

## Project Files
- `src/questioner/all-together.py`: Main script that orchestrates the interaction with ChatGPT, runs the questioner and answer modules, and handles the flow of generating questions and prompts.
- `src/questioner/questioner.py`: Script that generates a meta-question based on the project file structure and creates a prompt to ask ChatGPT which files it needs to examine in order to answer the user question.
- `src/questioner/answer.py`: Script responsible for constructing the final prompt by compiling information from project files based on the file list provided by `questioner.py`.
- `pyproject.toml`: File listing the project dependencies necessary for running the scripts. Install with `pip install -e .` (or `pip install -e ".[dev]"` for development dependencies).

## How to Use
1. Ensure you have the required Python dependencies installed. You can install them using `pip install -r requirements.txt`.
2. Run the `all-together.py` script with the necessary command-line arguments:
   - `--path`: Path to the development project directory.
   - `--question`: The question you want answered related to the project.
3. The script will interact with ChatGPT, parse project files, and provide the final answer to the user's question.

## Usage Example
```
python3 all-together.py --path /path/to/project --question "Please write a README.md for this project"
```

Feel free to customize this README.md as per your project's specific requirements and add any additional information to provide more context.
