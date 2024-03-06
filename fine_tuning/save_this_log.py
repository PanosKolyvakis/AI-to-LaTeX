import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def parse_log_entry(log_entry):
    prompt_delimiter, response_delimiter = '~~~', '!-!'
    lines = log_entry.strip().split('\n')
    
    prompt, response = '', ''
    inside_prompt, inside_response = False, False

    for line in lines:
        if prompt_delimiter in line:
            inside_prompt = True
            inside_response = False
            if line.strip().startswith(prompt_delimiter):
                prompt += ' ' + line.split(prompt_delimiter)[1]
            continue

        if response_delimiter in line and not inside_response:
            inside_response = True
            inside_prompt = False
            if line.strip().startswith(response_delimiter):
                response += ' ' + line.split(response_delimiter)[1]
            continue

        if response_delimiter in line and inside_response:
            response_end_index = line.find(response_delimiter)
            if response_end_index != -1:
                response += ' ' + line[:response_end_index]
            break

        if inside_prompt:
            prompt += ' ' + line
        elif inside_response:
            response += ' ' + line

    return {
        "prompt": prompt.strip(),
        "completion": response.strip()
    }

def append_to_json(new_data, json_file_path='training_data.json'):
    # Load existing data from the JSON file
    if os.path.exists(json_file_path):
        with open(json_file_path, 'r') as file:
            try:
                data = json.load(file)
                print(data)
            except json.JSONDecodeError:
                data = []
    else:
        data = []

    # Append the new data
    data.append(new_data)

    # Write the updated data back to the JSON file
    with open(json_file_path, 'w') as file:
        json.dump(data, file, indent=4)

if __name__ == "__main__":
    # Example: Reading log entries from a file
    with open('app_logs.log', 'r') as file:
        logs = file.read()

    new_entry = parse_log_entry(logs)
    append_to_json(new_entry)

    
