import json
import os
import re


def iterate_file(root_folder):
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file == 'result.log' and file is not None:
                extract_violations(os.path.join(subdir, file))


def extract_violations(file_path):
    try:
        with open(file_path, 'r') as file:
            data = file.readlines()

        violations_set = set()
        for row in data:
            if 'Warning: Transaction-Ordering Dependency.' in row:
                match = re.search(r':(\d+):(\d+):', row)
                if match:
                    line = match.group(1)
                    violations_set.add(("Transaction-Ordering Dependence (TOD)", line))
        update_vulnerabilites(file_path, violations_set)
    except FileNotFoundError:
        print(f'File not found: {file_path}')


def update_vulnerabilites(file_path, violations_set):
    general_dir = os.path.dirname(file_path)
    result_file_path = os.path.join(general_dir, 'result.json')

    with open(result_file_path, 'r') as file:
        data = json.load(file)

    old_findings = data.get('findings', [])
    new_findings = []
    for finding in old_findings:
        name = finding.get('name', None)
        if not name == "Transaction-Ordering Dependence (TOD)":
            new_findings.append(finding)

    if old_findings:
        contract = old_findings[0].get('contract', None)
        filename = old_findings[0].get('filename', None)
        for violation in violations_set:
            new_findings.append({
                'contract': contract,
                'filename': filename,
                'name': violation[0],
                'line': int(violation[1]),
            })

        print(f"OLD: {old_findings}")
        print(f"NEW: {new_findings}")
        data['findings'] = new_findings
        with open(result_file_path, 'w') as file:
            json.dump(data, file, indent=4)


if __name__ == '__main__':

    root_folder = ""
    iterate_file(root_folder)
