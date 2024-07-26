import csv
import sys
import re
import pandas as pd
from collections import Counter

artifacts_file = "csvs/sample_of_interest.csv"
log_file = "vulnerabilities_log.csv"

csv.field_size_limit(sys.maxsize)


def extract_vulnerabilities_from_logs():
    log_df = pd.read_csv(log_file)
    artifact_df = pd.read_csv(artifacts_file)

    conkas_df = log_df[log_df['Tool'] == 'conkas']
    slither_df = log_df[log_df['Tool'] == 'slither']
    smartcheck_df = log_df[log_df['Tool'] == 'smartcheck']

    conkas_result = confront_vulnerabilities('conkas', conkas_df, artifact_df)
    slither_result = confront_vulnerabilities('slither', slither_df, artifact_df)
    smartcheck_result = confront_vulnerabilities('smartcheck', smartcheck_df, artifact_df)

    result = pd.concat([conkas_result, slither_result, smartcheck_result], ignore_index=True)
    result = result.sort_values(by='contract')
    get_unique_vulnerabilities(result)


def confront_vulnerabilities(tool, log_df, artifact_df):
    merged_df = log_df.merge(artifact_df, left_on='File name', right_on='contract', suffixes=('_log', '_artifact'))
    result_df = merged_df[['contract', 'Mapped_findings', 'tag']].copy()

    result_df['tool'] = tool

    # Applica la funzione per trovare le vulnerabilità comuni
    result_df['common_vulnerabilities'] = result_df.apply(find_common_vulnerabilities, axis=1)
    result_df = result_df.dropna(subset=['common_vulnerabilities'])

    print(f"\nresult df: {len(result_df)}\n")
    return result_df


def find_common_vulnerabilities(row):
    findings_set = set(v.strip() for v in row['Mapped_findings'].split(';') if ': ' in v)
    tag_set = set(v.strip() for v in row['tag'].split(';') if ': ' in v)
    common_vulnerabilities = []

    if len(findings_set) > 0 and len(tag_set) > 0:
        print(f"findings: {findings_set}")
        print(f"tag: {tag_set}")
        for finding in findings_set:
            f_line, f_vuln = finding.split(':')
            if f_line != 'none':
                for tag in tag_set:
                    t_line, t_vuln = tag.split(':')
                    if re.match(r'^\d+-\d+', f_line):
                        start, end = map(int, f_line.split('-'))
                        t_line = int(t_line)
                        if start <= t_line <= end and t_vuln == f_vuln:
                            common_vulnerabilities.append(tag)
                    elif int(t_line) == int(f_line) and f_vuln == t_vuln:
                        common_vulnerabilities.append(tag)
        print(common_vulnerabilities)

    common_vulnerabilities = set(common_vulnerabilities)
    return '; '.join(common_vulnerabilities) if common_vulnerabilities else None


def get_unique_vulnerabilities(result_df):
    unique_vulnerabilities = {
        'conkas': {
            'access_control': 0,
            'arithmetic': 0,
            'denial_service': 0,
            'reentrancy': 0,
            'unchecked_low_calls': 0,
            'bad_randomness': 0,
            'front_running': 0,
            'time_manipulation': 0,
            'short_addresses': 0
        },
        'slither': {
            'access_control': 0,
            'arithmetic': 0,
            'denial_service': 0,
            'reentrancy': 0,
            'unchecked_low_calls': 0,
            'bad_randomness': 0,
            'front_running': 0,
            'time_manipulation': 0,
            'short_addresses': 0
        },
        'smartcheck': {
            'access_control': 0,
            'arithmetic': 0,
            'denial_service': 0,
            'reentrancy': 0,
            'unchecked_low_calls': 0,
            'bad_randomness': 0,
            'front_running': 0,
            'time_manipulation': 0,
            'short_addresses': 0
        },
    }

    total = 0
    group_df = result_df.groupby('contract')
    print(f"LEN OF GROUP DF: {len(group_df)}")
    for contract, group in group_df:
        print(f"\nContract: {contract}")
        common = []

        for _, row in group.iterrows():
            print(row['tool'], row['contract'], row['common_vulnerabilities'])
            vulns = row['common_vulnerabilities'].split(';')
            common.extend([vuln.strip() for vuln in vulns])
        print(f"common: {common}")
        vuln_counts = Counter(common)
        unique_vulns = [vuln.strip() for vuln in common if vuln_counts[vuln] == 1]
        print(f"unique: {unique_vulns}")

        if unique_vulns:
            for _, row in group.iterrows():
                vulnerabilities = set(row['common_vulnerabilities'].split(';'))
                print(f"vulnerabilities: {vulnerabilities}")
                for vulnerability in vulnerabilities:
                    if vulnerability.strip() in unique_vulns:
                        print(f"Tool: {row['tool']}")
                        tool = row['tool']
                        vuln = vulnerability.split(': ')[1]
                        unique_vulnerabilities[tool][vuln] += 1
                        total += 1

    print(f"\nRESULTS:"
          f"\nconkas{unique_vulnerabilities['conkas']}\n"
          f"\nslither{unique_vulnerabilities['slither']}\n"
          f"\nsmartcheck{unique_vulnerabilities['smartcheck']}\n"
          f"\nTotal: {total}")


if __name__ == '__main__':
    extract_vulnerabilities_from_logs()
