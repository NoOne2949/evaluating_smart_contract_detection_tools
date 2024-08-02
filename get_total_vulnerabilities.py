import csv
import sys
import re
import pandas as pd
from collections import Counter

artifacts_file = "csvs/sample_of_interest_without_arithmetic.csv"
log_file = "vulnerabilities_log_without_arithmetic.csv"

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
    return result_df


def find_common_vulnerabilities(row):
    findings_set = set(v.strip() for v in row['Mapped_findings'].split(';') if ': ' in v)
    tag_set = set(v.strip() for v in row['tag'].split(';') if ': ' in v)
    common_vulnerabilities = []

    if len(findings_set) > 0 and len(tag_set) > 0:
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

    common_vulnerabilities = set(common_vulnerabilities)
    return '; '.join(common_vulnerabilities) if common_vulnerabilities else None


def get_unique_vulnerabilities(result_df):
    total = 0
    group_df = result_df.groupby('contract')
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

        # if two or more tools found same vuln is ONLY a plus one for every tool
        total += sum(1 for vuln, count in vuln_counts.items() if count > 1)
        if unique_vulns:
            total += 1

    print(f"\nTotal: {total}")


if __name__ == '__main__':
    extract_vulnerabilities_from_logs()
