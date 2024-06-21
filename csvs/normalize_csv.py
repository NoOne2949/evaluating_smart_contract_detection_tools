import csv

from parse_vulnerability import parse_artifact_vulnerability, strip_vulnerability

artifacts_file = "sample_of_interest.csv"


def check_file():
    with open(artifacts_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        artifacts = list(reader)

    for row in artifacts:
        log = row['tag']
        if log != 'no' and log != 'FP':
            artifact = strip_vulnerability(log)
            parsed = []
            for line, vuln in artifact:
                parsed_vuln = parse_artifact_vulnerability(vuln)
                if parsed_vuln is None:
                    print(vuln)
                    return False
                else:
                    parsed.append(parsed_vuln)
    return True


def write_file():
    parsed_file = []
    with open(artifacts_file, 'r', newline='') as infile:
        reader = csv.DictReader(infile)
        artifacts = list(reader)

        for row in artifacts:
            log = row['tag']
            if log != 'no' and log != 'FP':
                artifact = strip_vulnerability(log)
                parsed = []
                for line, vuln in artifact:
                    parsed_vuln = parse_artifact_vulnerability(vuln)
                    if parsed_vuln is None:
                        print(vuln)
                        return False
                    else:
                        parsed.append(f"{line}: {parsed_vuln}")
                row['tag'] = '; '.join(parsed)
            parsed_file.append(row)

    if parsed_file is not None:
        with open(artifacts_file, 'w', newline='') as outfile:
            fieldnames = artifacts[0].keys()
            writer = csv.DictWriter(outfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(parsed_file)

    return True


if __name__ == '__main__':
    if check_file():
        write_file()
