import json
import os
import random

from vulneability_mapping import addVulnerability

def process_json_files(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            if file == "result.json":
                file_path = os.path.join(root, file)
                with open(file_path, 'r') as json_file:
                    json_content = json.load(json_file)
                    print(f"Processing file: {file_path}")
                    addVulnerability(json_content)


if __name__ == '__main__':
    directory = r"results/"
    process_json_files(directory)
