import json
import os
import random

from vulneability_mapping import addVulnerability


def generate_json():
    jsonlist = []
    vulnerabilities = [
        "access_control", "arithmetic", "denial_service", "reentrancy",
        "unchecked_low_calls", "bad_randomness", "front_running",
        "time_manipulation", "short_addresses", "Other", "Ignore"
    ]

    for i in range(100):
        vulnerability_index = random.randint(2, 12)
        vulnerability_key = vulnerabilities[vulnerability_index - 2]

        json_data = {"Tools": "Tool" + str(i), "Vulnerability name": "Vulnerability" + str(i), "access_control": False,
                     "arithmetic": False, "denial_service": False, "reentrancy": False, "unchecked_low_calls": False,
                     "bad_randomness": False, "front_running": False, "time_manipulation": False,
                     "short_addresses": False, "Other": False, "Ignore": False, vulnerability_key: True}
        jsonlist.append(json_data)

    with open("generated.json", 'w') as json_file:
        json.dump(jsonlist, json_file, indent=4)


if __name__ == '__main__':
    if not os.path.exists("generated.json"):
        print("Generating STAB JSON...")
        generate_json()
        print("STAB JSON generated.")

    print("\nStarted adding vulnerabilities...")
    with open("generated.json", 'r') as json_file:
        datas = json.load(json_file)
        for idx, data in enumerate(datas, start=1):
            print(f"Processing item {idx}/{len(datas)}...")
            addVulnerability(data)
    print("\nAdding vulnerabilities completed.")

    print("\nRetrying adding vulnerabilities to check for duplicates...")
    with open("generated.json", 'r') as json_file:
        datas = json.load(json_file)
        for idx, data in enumerate(datas, start=1):
            print(f"Processing item {idx}/{len(datas)}...")
            addVulnerability(data)
    print("\nTesting completed.")

