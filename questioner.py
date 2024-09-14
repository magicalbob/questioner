#!/usr/bin/env python3
import os
import openai
import argparse

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_file_structure(project_path):
    """Walk through the project directory and return a list of file paths."""
    file_paths = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            file_paths.append(os.path.join(root, file))
    return file_paths

def construct_meta_question(file_structure, user_question):
    """Construct the 'question about a question' to ask ChatGPT."""
    file_list_str = '\n'.join(file_structure)
    meta_question = (
        f"I have the following project structure:\n\n{file_list_str}\n\n"
        f"The user wants to know: '{user_question}'. "
        f"Which files from the project do you need to look at to answer the user's question?"
    )
    return meta_question

def ask_chatgpt(question):
    """Send the question to ChatGPT and return the response."""
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are an assistant who helps with software development."},
            {"role": "user", "content": question}
        ]
    )
    return response.choices[0].message['content']

def get_files_to_include(response, project_path):
    """Extract file names from ChatGPT's response and return their paths."""
    # List of files ChatGPT suggested
    suggested_files = []

    # Extract file names from ChatGPT's response
    for line in response.split('\n'):
        line = line.strip()
        if line.startswith('**') and '**' in line:  # e.g., **app.py**
            # Extract the file name by stripping out ** markers
            file_name = line.strip('*').strip()
            suggested_files.append(file_name)

    # Now match those file names to actual files in the project directory
    file_list = []
    for root, dirs, files in os.walk(project_path):
        for file in files:
            if file in suggested_files:
                file_list.append(os.path.join(root, file))

    return file_list

def read_files(file_paths):
    """Read the contents of the files and return them as a dictionary."""
    file_contents = {}
    for file in file_paths:
        if os.path.isfile(file):  # Ensure we're reading only files, not directories
            try:
                with open(file, 'r') as f:
                    content = f.read()
                file_contents[file] = content
            except Exception as e:
                file_contents[file] = f"Error reading file: {e}"
        else:
            file_contents[file] = f"Error: {file} is not a file."
    return file_contents


def construct_final_question(user_question, file_contents):
    """Construct the final question with the user's question and file contents."""
    files_info = "\n".join(
        f"File: {file}\nContents:\n{content}\n{'-'*40}" for file, content in file_contents.items()
    )
    
    final_question = (
        f"The user asked the following question:\n'{user_question}'\n\n"
        f"Here are the contents of the relevant files:\n\n{files_info}\n\n"
        "Based on this, can you provide the answer to the user's question?"
    )
    return final_question

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description="Ask ChatGPT a question about a development project.")
    parser.add_argument('-path', required=True, help="Path to the development project")
    parser.add_argument('-question', required=True, help="The question you want answered")
    args = parser.parse_args()

    # Step 1: Get the project file structure
    project_path = args.path
    user_question = args.question
    file_structure = get_file_structure(project_path)

    # Step 2: Construct the meta-question to ask ChatGPT
    meta_question = construct_meta_question(file_structure, user_question)

    # Step 3: Ask ChatGPT which files it needs
    print("Asking ChatGPT which files are needed...")
    meta_response = ask_chatgpt(meta_question)
    print(f"ChatGPT suggests the following files:\n{meta_response}")

    # Step 4: Extract file names from ChatGPT's response and read their contents
    files_to_include = get_files_to_include(meta_response, project_path)
    if not files_to_include:
        print("ChatGPT did not suggest any valid files.")
        return

    print(f"Reading the following files: {files_to_include}")
    file_contents = read_files([os.path.join(project_path, file) for file in files_to_include])

    # Step 5: Construct the final question with file contents
    final_question = construct_final_question(user_question, file_contents)
    print("<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
    print(final_question)
    print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")

    # Step 6: Ask ChatGPT the final question with file contents
    print("Asking ChatGPT the final question...")
    final_response = ask_chatgpt(final_question)
    print(f"ChatGPT's answer:\n{final_response}")

if __name__ == "__main__":
    main()

