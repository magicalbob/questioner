#!/usr/bin/env python3
import os
import json
import argparse
import subprocess
import openai
import tempfile
import time

# Function to ask ChatGPT and return the response
def ask_chatgpt(prompt):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    response = None
    retries = 5
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0125",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
            )
            return response.choices[0].message['content']
        except openai.error.RateLimitError:
            if i < retries - 1:
                time.sleep(10)  # wait before retrying
            else:
                raise Exception("API is overloaded, please try again later.")

def save_to_temp_file(content, increment):
    """Save content to a temporary file with an incrementing number."""
    temp_file_path = f'/tmp/all-together.prompt.{increment}'
    with open(temp_file_path, 'w') as temp_file:
        temp_file.write(content)
    return temp_file_path

def validate_json(file_path):
    """Validate JSON content from a file."""
    with open(file_path, 'r') as f:
        try:
            json.load(f)  # Attempt to load the JSON
            return True
        except json.JSONDecodeError:
            return False

def clean_json_response(file_path):
    """Remove code block markers from the JSON response."""
    with open(file_path, 'r') as f:
        lines = f.readlines()
    
    # Remove the first and last lines if they match the code block markers
    if lines[0].startswith("```json") and lines[-1].strip() == "```":
        lines = lines[1:-1]  # Remove first and last line

    with open(file_path, 'w') as f:
        f.writelines(lines)

def main():
    parser = argparse.ArgumentParser(description="Run questioner and answer modules, and interact with ChatGPT.")
    parser.add_argument('--path', required=True, help='Path to the development project')
    parser.add_argument('--question', required=True, help='The question you want answered')
    args = parser.parse_args()

    # Step 1: Run questioner.py to get the meta-question
    questioner_command = ['python3', 'questioner.py', '-path', args.path, '-question', args.question]
    result = subprocess.run(questioner_command, capture_output=True, text=True)
    meta_question = result.stdout.strip()

    # Save the meta-question to a temporary file
    increment = 1
    save_to_temp_file(meta_question, increment)
    print(f"Meta-question saved to /tmp/all-together.prompt.{increment}")

    # Step 2: Submit the meta-question to ChatGPT
    print("Asking ChatGPT for file list...")
    file_list_json = ask_chatgpt(meta_question)

    # Save the response from ChatGPT (file list)
    increment += 1
    file_list_path = save_to_temp_file(file_list_json, increment)
    print(f"File list response saved to /tmp/all-together.prompt.{increment}")

    # Clean the JSON response
    clean_json_response(file_list_path)

    # Validate the JSON file
    if not validate_json(file_list_path):
        print("Invalid JSON response, resubmitting the meta-question...")
        file_list_json = ask_chatgpt(meta_question)
        increment += 1
        file_list_path = save_to_temp_file(file_list_json, increment)
        print(f"File list response saved to /tmp/all-together.prompt.{increment}")
        clean_json_response(file_list_path)

    # Load the file list from JSON
    with open(file_list_path, 'r') as f:
        file_list = json.load(f)

    # Step 3: Run answer.py to construct the final prompt
    answer_command = ['python3', 'answer.py', '--path', args.path, '--file-list', file_list_path, '--question', args.question]
    answer_result = subprocess.run(answer_command, capture_output=True, text=True)
    final_prompt = answer_result.stdout.strip()

    # Save the final prompt to a temporary file
    increment += 1
    save_to_temp_file(final_prompt, increment)
    print(f"Final prompt saved to /tmp/all-together.prompt.{increment}")

    # Step 4: Submit the final prompt to ChatGPT
    print("Asking ChatGPT for the final answer...")
    final_answer = ask_chatgpt(final_prompt)

    # Save the final answer to a temporary file
    increment += 1
    save_to_temp_file(final_answer, increment)
    print(f"Final answer response saved to /tmp/all-together.prompt.{increment}")

    # Output the final answer
    print("Final Answer from ChatGPT:")
    print(final_answer)

if __name__ == "__main__":
    main()
