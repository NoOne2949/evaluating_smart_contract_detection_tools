import re

import solcx
import os

solcx.install_solc('0.8.0')
solcx.set_solc_version('0.8.0')


def get_solc_version_from_pragma(source_code):
    match = re.search(r'pragma solidity\s+([^\s;]+)', source_code)
    if match:
        return match.group(1).strip('^')
    return None

def compile_sol_to_hex(sol_file_path):
    # Read Solidity source code
    with open(sol_file_path, 'r') as file:
        source_code = file.read()

    solc_version = get_solc_version_from_pragma(source_code)
    if not solc_version:
        raise ValueError("Could not find the pragma solidity version in the source file")

    # Install and set the Solidity compiler version
    solcx.install_solc(solc_version)
    solcx.set_solc_version(solc_version)

    # Compile Solidity source code
    compiled_sol = solcx.compile_source(
        source_code,
        output_values=['abi', 'bin']
    )

    # Extract the contract name
    contract_id, contract_interface = compiled_sol.popitem()
    contract_bin = contract_interface['bin']

    # Save the .hex file
    hex_file_path = os.path.splitext(sol_file_path)[0] + '.hex'
    with open(hex_file_path, 'w') as hex_file:
        hex_file.write(contract_bin)

    print(f'Compiled {sol_file_path} to {hex_file_path}')
    return hex_file_path