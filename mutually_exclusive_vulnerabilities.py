import csv
import sys
import re
import pandas as pd
from confront_vulnerability import check_vuln

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

    print(len(result_df))
    return result_df


def find_common_vulnerabilities(row):
    findings_set = set(v for v in row['Mapped_findings'].split(';') if ': ' in v)
    tag_set = set(v for v in row['tag'].split(';') if ': ' in v)
    common_vulnerabilities = []

    for finding in findings_set:
        finding_line = finding.strip().split(': ')[0]
        finding_vuln = finding.strip().split(': ')[1]

        if re.match(r'^\d+-\d+', finding_line):
            line_start = finding_line.strip('-')[0]
            line_end = finding_line.strip('-')[1]

            for tag in tag_set:
                tag_line = tag.strip().split(': ')[0]
                tag_vuln = tag.strip().split(': ')[1]
                if line_start <= tag_line <= line_end and finding_vuln == tag_vuln:
                    common_vulnerabilities.append(tag)
        else:
            for tag in tag_set:
                if finding == tag:
                    common_vulnerabilities.append(tag)

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

    group_df = result_df.groupby('contract')
    for contract, group in group_df:
        print(f"\nContract: {contract}")
        common = []
        unique_values = None

        for _, row in group.iterrows():
            print(row['tool'], row['contract'], row['common_vulnerabilities'])
            common.append(set(row['common_vulnerabilities'].split(';')))
        if len(common) == 1:
            unique_values = common[0]
        elif len(common) == 2:
            unique_values = common[0] ^ common[1]
        elif len(common) == 3:
            union_all = common[0].union(*common[1:])
            intersection_all = common[0].intersection(*common[1:])
            unique_values = union_all - intersection_all

        if unique_values:
            for _, row in group.iterrows():
                vulnerabilities = set(row['common_vulnerabilities'].split(';'))
                for vulnerability in vulnerabilities:
                    if vulnerability in unique_values:
                        tool = row['tool']
                        vuln = vulnerability.split(': ')[1]
                        unique_vulnerabilities[tool][vuln] += 1

        print(common)
        print(unique_values)
    print(f"\nRESULTS:"
          f"\nconkas{unique_vulnerabilities['conkas']}"
          f"\nslither{unique_vulnerabilities['slither']}"
          f"\nsmartcheck{unique_vulnerabilities['smartcheck']}")
    total = 0
    for tool in unique_vulnerabilities.keys():
        for key in unique_vulnerabilities[tool].keys():
            total += unique_vulnerabilities[tool][key]
    print("Total: ", total)


if __name__ == '__main__':
    extract_vulnerabilities_from_logs()
