import pandas as pd
import matplotlib.pyplot as plt
import json

gpt_sb_results_vulnerabilities = []
sb_results_manually_tagged_vulnerabilities = []


def analyzed_gpt_sb_result(address, vulnerability_in_code):
    global gpt_sb_results_vulnerabilities
    if ":" in vulnerability_in_code:
        if ";" in vulnerability_in_code:
            vulns = vulnerability_in_code.split(";")

            for v in vulns:
                if v != '':
                    v = v.strip()
                    splitted = v.split(':')
                    line = splitted[0]
                    try:
                        vulnerability = splitted[1]
                    except:

                        obj = {
                            "line": line,
                            "name": address,
                            "vulnerability": 'error in gpt response',
                        }
                        gpt_sb_results_vulnerabilities.append(obj)

                    obj = {
                        "line": line,
                        "name": address,
                        "vulnerability": vulnerability,
                    }
                    gpt_sb_results_vulnerabilities.append(obj)
        else:

            obj = {
                "line": 'NO',
                "vulnerability": 'NO',
                "name": address
            }
            gpt_sb_results_vulnerabilities.append(obj)

    else:

        if 'unable' in vulnerability_in_code.lower():

            obj = {
                "line": 'NO',
                "vulnerability": 'NO',
                "name": address
            }
            gpt_sb_results_vulnerabilities.append(obj)

        elif 'no' in vulnerability_in_code.lower():

            obj = {
                "line": 'NO',
                "vulnerability": 'NO',
                "name": address
            }
            gpt_sb_results_vulnerabilities.append(obj)

        else:
            print(address)


def analyzed_sb_result(address, vulnerabilities):
    pass


### main
# sb_result_path = 'smartbugs_results.csv'
gpt_sb_result_path = 'gpt_smartbugs_results.csv'

gpt_sb_result_df = pd.read_csv(gpt_sb_result_path)
# sb_result_df = pd.read_csv(sb_result_path)

for index, row in gpt_sb_result_df.iterrows():
    address = row["Path"]
    vulnerabilities = row["Vulnerabilities"]
    analyzed_gpt_sb_result(address, vulnerabilities)

print(len(gpt_sb_results_vulnerabilities))

# for index, row in sb_result_df.iterrows():
#     address = row["Path"]
#     vulnerabilities = row["Vulnerabilities"]
#     analyzed_sb_result(address, vulnerabilities)
#     pass
