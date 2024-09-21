#!/usr/bin/env python3
import os
import json
import subprocess
import tempfile
import openai
import argparse

def ask_chatgpt(question):
    openai.api_key = os.getenv("OPENAI_API_KEY")
    actual_question = f"Considering the following project files and their contents:\n{question}\nPlease provide suggestions on how to make this project more modular. Include HTML tags for formatting."
    retries = 5
    
    for i in range(retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a helpful assistant with expertise in software architecture."},
                    {"role": "user", "content": actual_question}
                ],
            )
            answer = response['choices'][0]['message']['content']
            return answer
        except Exception as e:
            print(f"Error: {e}")
            if isinstance(e, openai.error.RateLimitError) and i < retries - 1:
                time.sleep(10)
            else:
                return "API is overloaded, please try again later."

def run_questioner(path, question):
    """Run the questioner script and get the JSON output."""
    result = subprocess.run(
        ['python3', 'questioner.py', '-path', path, '-question', question],
        capture_output=True,
        text=True
    )
    return result.stdout

def main():
    parser = argparse.ArgumentParser(description="Integrate questioner and answer modules.")
    parser.add_argument('--path', required=True, help='Path to the development project')
    parser.add_argument('--question', required=True, help='The question you want answered')
    args = parser.parse_args()

    # Step 1: Run questioner.py and get the meta-question
    meta_question = run_questioner(args.path, args.question)

    # Step 2: Ask ChatGPT the meta-question and get the JSON output
    print("Asking ChatGPT...")
    json_output = ask_chatgpt(meta_question)
    
    # Step 3: Save the output to a temporary JSON file
    with tempfile.NamedTemporaryFile(delete=False, suffix='.json') as temp_file:
        temp_file.write(json_output.encode('utf-8'))
        temp_file_path = temp_file.name

    # Step 4: Run answer.py with the path, question, and temp JSON file
    answer_result = subprocess.run(
        ['python3', 'answer.py', '--path', args.path, '--file-list', temp_file_path, '--question', args.question],
        capture_output=True,
        text=True
    )

    # Step 5: Get the final answer from ChatGPT
    final_answer = ask_chatgpt(answer_result.stdout)
    
    # Output the final answer
    print("Final Answer from ChatGPT:")
    print(final_answer)

if __name__ == "__main__":
    main()
