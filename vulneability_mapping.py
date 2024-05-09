import csv

file_name = "smartbugs-results/metadata/vulnerabilities_mapping.csv"


def convertToCSV(json_data):
    return [
        json_data["Tools"],
        json_data["Vulnerability name"],
        'TRUE' if json_data["access_control"] else None,
        'TRUE' if json_data["arithmetic"] else None,
        'TRUE' if json_data["denial_service"] else None,
        'TRUE' if json_data["reentrancy"] else None,
        'TRUE' if json_data["unchecked_low_calls"] else None,
        'TRUE' if json_data["bad_randomness"] else None,
        'TRUE' if json_data["front_running"] else None,
        'TRUE' if json_data["time_manipulation"] else None,
        'TRUE' if json_data["short_addresses"] else None,
        'TRUE' if json_data["Other"] else None,
        'TRUE' if json_data["Ignore"] else None,
    ]


def addVulnerability(file):
    line = convertToCSV(file)

    row_exist = False
    with open(file_name, 'r', newline='') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[:2] == line[:2]:
                row_exist = True
                break

    if not row_exist:
        with open(file_name, 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(line)
