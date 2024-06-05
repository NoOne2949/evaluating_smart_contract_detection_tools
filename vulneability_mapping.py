import csv
import json
import os

vulnerability_file = "smartbugs-results/metadata/vulnerabilities_mapping.csv"
vulnerability_log = "vulnerabilities_log.csv"


def check_line(vulnerability_name):
    with open(vulnerability_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if vulnerability_name in row:
                return True
    return False


def process_vulnerabilities(tool, file_name, vulnerabilities):
    for vulnerability in vulnerabilities:
        if type(vulnerability) is dict and vulnerability.get("name"):
            vulnerability_name = vulnerability.get("name")
            vulnerability_line = vulnerability.get("line")

            if vulnerability_name == 'secure':
                return

            print(f"{tool}, {file_name}, {vulnerability_name}, {vulnerability_line}")
            if not check_line(vulnerability_name):
                with open(vulnerability_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([tool, vulnerability_name])

            with open(vulnerability_log, 'a', newline='') as file:
                writer = csv.writer(file)
                writer.writerow([tool, file_name, vulnerability_line, vulnerability_name])


def parser(tool, file, json_content):
    # process_vulnerabilities(tool, json_content.get("errors", []), "error")
    # process_vulnerabilities(tool, json_content.get("fails", []), "fail")
    process_vulnerabilities(tool, file, json_content.get("findings", []))


def process_json_files(directory):
    # initialize vulnerability log file
    if not os.path.exists(vulnerability_log):
        with open(vulnerability_log, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tool", "File name", "Vulnerability line", "Vulnerability name"])

    for dir_name in os.listdir(directory):
        tool = dir_name.lower()
        print(f'\nSTARTED {tool.upper()} RESULT PARSING')
        for root, _, files in os.walk(os.path.join(directory, tool)):
            for file in files:
                if file == "result.json":
                    file_path = os.path.join(root, file)
                    file_name = os.path.basename(root)

                    with open(file_path, 'r') as json_file:
                        json_content = json.load(json_file)
                        print(f"Processing file: {file_name}")
                        parser(tool, file_name, json_content)
