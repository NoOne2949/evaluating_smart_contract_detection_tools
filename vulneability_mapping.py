import csv

vulnerability_file = "smartbugs-results/metadata/vulnerabilities_mapping.csv"


def check_line(vulnerability_name):
    with open(vulnerability_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if vulnerability_name in row:
                return True
    return False


def process_vulnerabilities(tool, vulnerabilities, vulnerability_type):
    for vulnerability in vulnerabilities:
        if type(vulnerability) is dict and vulnerability.get("name"):
            vulnerability_name = vulnerability.get("name")

            if vulnerability_name == 'secure':
                return

            print(f"{tool}, {vulnerability_type}, {vulnerability_name}")
            if not check_line(vulnerability_name):
                with open(vulnerability_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow([tool, vulnerability_name])

def parser(tool, json_content):
    process_vulnerabilities(tool, json_content.get("errors", []), "error")
    process_vulnerabilities(tool, json_content.get("fails", []), "fail")
    process_vulnerabilities(tool, json_content.get("findings", []), "finding")


def addVulnerability(tool, file):
    parser(tool, file)
