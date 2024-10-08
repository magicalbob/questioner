#!/usr/bin/env python3
import os
import argparse

def get_file_structure(project_path):
    """Walk through the project directory and return a list of file paths, ignoring irrelevant ones."""
    file_paths = []
    ignore_dirs = ['.git', '__pycache__', '.scannerwork']  # Add more directories as needed
    for root, dirs, files in os.walk(project_path):
        # Skip ignored directories
        dirs[:] = [d for d in dirs if d not in ignore_dirs]
        for file in files:
            # Skip hidden files (starting with .)
            if not file.startswith('.'):
                rel_dir = os.path.relpath(root, project_path)
                rel_file = os.path.join(rel_dir, file) if rel_dir != "." else file
                file_paths.append(rel_file)
    return file_paths

def construct_meta_question(file_structure, user_question):
    """Construct the 'question about a question' to ask ChatGPT."""
    file_list_str = '\n'.join(file_structure)
    meta_question = (
        f"I have the following project structure:\n\n{file_list_str}\n\n"
        f"The user wants to know: '{user_question}'. "
        f"Which files from the project do you need to look at to answer the user's question?"
        "Please answer in JSON like this [{'file1': 'name_of_file1'}, {'file2': 'name_of_file2'} ... {'fileN': 'name_of_fileN'}]. It is important that keys always start with file."
    )
    return meta_question

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Generate a meta-question about a development project.")
    parser.add_argument('--path', required=True, help="Path to the development project")
    parser.add_argument('--question', required=True, help="The question you want answered")
    args = parser.parse_args()

    # Step 1: Get the project file structure
    project_path = args.path
    user_question = args.question
    file_structure = get_file_structure(project_path)

    # Step 2: Construct and print the meta-question
    meta_question = construct_meta_question(file_structure, user_question)
    print("Meta-question to ask ChatGPT:")
    print("========================================")
    print(meta_question)
    print("========================================")

if __name__ == "__main__":
    main()

