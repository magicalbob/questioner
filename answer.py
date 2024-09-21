import json
import os
import argparse

def construct_prompt(path, file_list, question):
    prompt_parts = [f"My project contains these files:"]
    
    for file_dict in file_list:
        for file_name in file_dict.values():
            file_path = os.path.join(path, file_name)
            try:
                with open(file_path, 'r') as f:
                    contents = f.read()
                prompt_parts.append(f"{file_name}:\n{contents}")
            except FileNotFoundError:
                prompt_parts.append(f"{file_name}: [File not found]")
    
    prompt_parts.append(f"I want to know: {question}")
    return "\n\n".join(prompt_parts)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Construct a prompt from project files.')
    parser.add_argument('--path', required=True, help='Path to the directory containing the files.')
    parser.add_argument('--file-list', required=True, help='Path to the JSON file listing the files.')
    parser.add_argument('--question', required=True, help='The question to ask about the project.')
    
    args = parser.parse_args()

    # Load the file list from JSON
    with open(args.file_list, 'r') as f:
        file_list = json.load(f)

    # Construct and print the prompt
    prompt = construct_prompt(args.path, file_list, args.question)
    print(prompt)
