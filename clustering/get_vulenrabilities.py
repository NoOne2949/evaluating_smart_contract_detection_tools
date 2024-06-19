import pandas as pd


def analyze_sb_results(vulnerability_in_code, name):
    global sb_gpt_results_vulnerabilities
    if ";" in vulnerability_in_code:
        vulns = vulnerability_in_code.split(";")

        for v in vulns:
            if v != '':
                v = v.strip()
                splitted = v.split(':')
                line = splitted[0]
                vulnerability = splitted[1]
                obj = {
                    "line": line,
                    #"name": name,
                    "vulnerability": vulnerability
                }
                print(obj)
                exit(1)
               # sb_gpt_results_vulnerabilities.append(obj)
    else:
        obj = {
            "line": 'NO',
            "vulnerability": 'NO',
            #"name": name
        }
        #sb_gpt_results_vulnerabilities.append(obj)


sb_results_path = '../csvs/AggregatedArtifacts.csv'
sb_results_df = pd.read_csv(sb_results_path)

for index, row in sb_results_df.iterrows():
    analyze_sb_results(row["labeling"], row["address"])
