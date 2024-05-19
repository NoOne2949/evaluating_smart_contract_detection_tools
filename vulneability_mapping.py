import csv

vulnerability_file = "smartbugs-results/metadata/vulnerabilities_mapping.csv"


def check_line(vulnerability_name):
    with open(vulnerability_file, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if vulnerability_name in row:
                return True
    return False


def process_vulnerabilities(vulnerabilities, vulnerability_type):
    for vulnerability in vulnerabilities:
        if vulnerability.get("name"):
            vulnerability_name = vulnerability.get("name")
            category = vulnerability.get("category")
            print(f"{vulnerability_type}, {category}, {vulnerability_name}")
            if not check_line(vulnerability_name):
                with open(vulnerability_file, 'a', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(['semgrep', vulnerability_name])


def semgrep(json_content):
    process_vulnerabilities(json_content.get("errors", []), "error")
    process_vulnerabilities(json_content.get("fails", []), "fail")
    process_vulnerabilities(json_content.get("findings", []), "finding")


def addVulnerability(file):
    semgrep(file)
