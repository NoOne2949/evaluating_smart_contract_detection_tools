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


def compileContract(directory):
    compiled_contracts = []
    not_compiled_contracts = []

    for root, _, files in os.walk(directory):
        for file in files:
            compiled = compile_sol_to_hex(os.path.join(directory, file))
            if compiled is True:
                compiled_contracts.append(file)
            else:
                not_compiled_contracts.append(file)

    print(f"\ncontracts compiled: {len(compiled_contracts)}")
    for contract in not_compiled_contracts:
        print(f"contract compiled: {contract}")

    print(f"\ncontracts not compiled: {len(not_compiled_contracts)}")
    for contract in not_compiled_contracts:
        print(f"contract not compiled: {contract}")


if __name__ == '__main__':
    sol_file_path = 'dataset/'
    compileContract(sol_file_path)
