import json
import os
import random

from compile import compile_sol_to_hex
from vulneability_mapping import addVulnerability

def process_json_files(directory):
    for dir_name in os.listdir(directory):
        tool = dir_name.lower()
        print(f'STARTED {tool.upper()} RESULT PARSING')
        for root, _, files in os.walk(os.path.join(directory, tool)):
            for file in files:
                if file == "result.json":
                    file_path = os.path.join(root, file)
                    with open(file_path, 'r') as json_file:
                        json_content = json.load(json_file)
                        print(f"Processing file: {file_path}")
                        addVulnerability(tool, json_content)


if __name__ == '__main__':
    directory = r"results/"
    process_json_files(directory)

    # sol_file_path = 'dataset/'
    # compile_sol_to_hex(sol_file_path)
