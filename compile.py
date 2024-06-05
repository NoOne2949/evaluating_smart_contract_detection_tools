import re

import solcx
import os

solcx.install_solc('0.8.0')
output_directory = 'dataset_compiled'

compiled_contracts = []
not_compiled_contracts = []


def get_solc_version_from_pragma(source_code):
    match = re.search(r'pragma solidity\s+([^\s;]+)', source_code)
    if match:
        return match.group(1).strip('^')
    return None


def is_version_less_than(version, comparison_version):
    version_parts = [int(part) for part in version.split('.')]
    comparison_parts = [int(part) for part in comparison_version.split('.')]
    return version_parts < comparison_parts


def compile_sol_to_hex(sol_file_path):
    try:
        with open(sol_file_path, 'r') as file:
            source_code = file.read()

        solc_version = get_solc_version_from_pragma(source_code)
        if not solc_version:
            raise ValueError("Could not find the pragma solidity version in the source file")

        if is_version_less_than(solc_version, '0.4.11'):
            solc_version = '0.4.11'

        solcx.install_solc(solc_version)
        solcx.set_solc_version(solc_version)

        compiled_sol = solcx.compile_source(
            source_code,
            output_values=['abi', 'bin']
        )

        contract_id, contract_interface = compiled_sol.popitem()
        contract_bin = contract_interface['bin']

        if not os.path.exists(output_directory):
            os.makedirs(output_directory)
        hex_file_path = os.path.join(output_directory, os.path.basename(os.path.splitext(sol_file_path)[0] + '.hex'))
        print(hex_file_path)
        with open(hex_file_path, 'w') as hex_file:
            hex_file.write(contract_bin)
        compiled_contracts.append(sol_file_path)
    except Exception as e:
        not_compiled_contracts.append(f"{e}: {sol_file_path}")


def compileContract(directory):
    for root, _, files in os.walk(directory):
        for file in files:
            compile_sol_to_hex(os.path.join(directory, file))

    print(f"\ncontracts compiled: {len(compiled_contracts)}")
    for contract in compiled_contracts:
        print(f"contract compiled: {contract}")

    print(f"\ncontracts not compiled: {len(not_compiled_contracts)}")
    for contract in not_compiled_contracts:
        print(f"contract not compiled: {contract}")
