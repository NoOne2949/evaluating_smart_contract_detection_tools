import json
import os

root_folder = '/home/kevin/PycharmProjects/tesi/results/securify'


def iterate_file():
    for subdir, _, files in os.walk(root_folder):
        for file in files:
            if file == 'live.json':
                extract_violations(os.path.join(subdir, file))


def extract_violations(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)

    # Iterare attraverso patternResults
    pattern_results = data.get('patternResults', {})
    violations_set = set()

    print(f"\nFOUND IN FILE {file_path}")
    for pattern, details in pattern_results.items():
        violations = details.get('violations', [])
        if violations:
            for line in violations:
                print(f"Violazione: {pattern}, Linea: {line}")
                violations_set.add((pattern, line))
    update_result(file_path, violations_set)


def update_result(file_path, violations_set):
    general_dir = os.path.dirname(os.path.dirname(os.path.dirname(file_path)))
    result_file_path = os.path.join(general_dir, 'result.json')

    with open(result_file_path, 'r') as file:
        data = json.load(file)

    findings_list = []

    print(f"OLD DATA: {data}")
    for violation in violations_set:
        findings_list.append({
            'filename': os.path.basename(general_dir),
            'name': violation[0],
            'line': violation[1],
        })
    data['findings'] = findings_list
    print(f"UPDATED DATA: {data}")
    with open(result_file_path, 'w') as file:
        json.dump(data, file, indent=4)


if __name__ == '__main__':
    iterate_file()
