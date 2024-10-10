import json
import os
import matplotlib.pyplot as plt
import pandas as pd

# Global variables
sb_gpt_curated_vulnerabilities = []
sb_durieux_curated_vulnerabilities = []
sb_gpt_results_vulnerabilities = []
sb_results_vulnerabilities = []

def analyze_sb_results(vulnerability_in_code, address):
    global sb_results_vulnerabilities
    if ";" in vulnerability_in_code:
        vulns = vulnerability_in_code.strip().split(";")
        for v in vulns:
            if v != '':
                v = v.strip()
                splitted = v.split(':')
                line = splitted[0]
                try:
                    vulnerability = splitted[1]
                    obj = {
                        "line": line,
                        "vulnerability": vulnerability,
                        "address": address
                    }
                    sb_results_vulnerabilities.append(obj)
                except IndexError:
                    pass  # Ignore malformed entries
    else:
        if vulnerability_in_code.strip() == 'S':
            obj = {
                "line": 'NO',
                "vulnerability": 'NO',
                "address": address
            }
            sb_results_vulnerabilities.append(obj)

def analyze_gpt_analyzed_sb_results(vulnerability_in_code, name):
    global sb_gpt_results_vulnerabilities
    if ";" in vulnerability_in_code:

        vulns = vulnerability_in_code.strip().split(";")
        for v in vulns:
            if v != '':
                v = v.strip()
                if len(v) <=1:
                    continue
                splitted = v.split(':')
                line = splitted[0]
                try:
                    vulnerability = splitted[1]
                    obj = {
                        "line": line,
                        "name": name,
                        "vulnerability": vulnerability
                    }
                    sb_gpt_results_vulnerabilities.append(obj)
                except IndexError:
                    print(name)
                    print(v)
    else:
        print('*********')
        obj = {
            "line": 'NO',
            "vulnerability": 'NO',
            "name": name
        }

        sb_gpt_results_vulnerabilities.append(obj)

def compare_results_on_sb_results():
    global sb_gpt_results_vulnerabilities, sb_results_vulnerabilities
    results_dict_gpt = {}
    results_dict_item = {}
    gpt_correct_analysis = []
    gpt_incorrect_analysis = []

    for item in sb_results_vulnerabilities:
        for gpt_item in sb_gpt_results_vulnerabilities:
            if gpt_item["name"] == item["address"]:
                if item["vulnerability"].strip().lower() in gpt_item["vulnerability"].strip().lower():
                    gpt_correct_analysis.append(gpt_item)
                else:
                    gpt_incorrect_analysis.append(gpt_item)

    # Create result dictionaries for JSON
    for gpt_item in gpt_correct_analysis:
        if gpt_item["name"] not in results_dict_gpt:
            results_dict_gpt[gpt_item["name"]] = []
        results_dict_gpt[gpt_item["name"]].append(gpt_item)

    for gpt_item in gpt_incorrect_analysis:
        if gpt_item["name"] not in results_dict_gpt:
            results_dict_gpt[gpt_item["name"]] = []
        results_dict_gpt[gpt_item["name"]].append(gpt_item)

    for item in sb_results_vulnerabilities:
        if item["address"] not in results_dict_item:
            results_dict_item[item["address"]] = []
        results_dict_item[item["address"]].append(item)

    # Save the results as JSON
    with open('sb_gpt_results.json', 'w') as f_gpt:
        json.dump(results_dict_gpt, f_gpt, indent=4)

    with open('sb_results.json', 'w') as f_item:
        json.dump(results_dict_item, f_item, indent=4)

# Main execution
path = os.getcwd()
print(path)

# Read SmartBugs curated results
smartbugs_curated = f"{path}/sb_curated/smartbugs_curated_revised.csv"
smartbugs_curated_df = pd.read_csv(smartbugs_curated)

# Read GPT analysis for SmartBugs
smartbugs_curated_gpt_df = pd.read_csv(f"{path}/sb_curated/sb_curated_gpt_analysis.csv")
print(smartbugs_curated_gpt_df.keys())
for index, row in smartbugs_curated_gpt_df.iterrows():
    vulnerability_in_code = row["Vulnerabilities"]
    name = row["Path"]
    #analyze_gpt_analyzed_smartbugs_curated(vulnerability_in_code.strip(), name, name)

# Read vulnerabilities from JSON
json_file_path = "sb_curated/vulnerabilities.json"
#read_and_print_json_properties(json_file_path)

# Analyze SmartBugs results
sb_results_path = f"{path}/sb_results/sbresult_manual_analysis.csv"
sb_results_df = pd.read_csv(sb_results_path)

gpt_sb_results_path = f"{path}/sb_results/smartbugs_results_gpt_analysis.csv"
gpt_sb_results_df = pd.read_csv(gpt_sb_results_path)

# Analyze GPT results
for index, row in gpt_sb_results_df.iterrows():
    tag = row["Vulnerabilities"]
    address = row["Path"]
    print(tag)
    analyze_gpt_analyzed_sb_results(tag, address)

# Analyze SB results
for index, row in sb_results_df.iterrows():
    if row["label"] == 'smartbugs_results':

        tag = row["tag"]
        address = row["contract"]
        analyze_sb_results(tag, address)

# Compare results on SmartBugs
compare_results_on_sb_results()

print("Results saved in sb_gpt_results.json and sb_results.json")
