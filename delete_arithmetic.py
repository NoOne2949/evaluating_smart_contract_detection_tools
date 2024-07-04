import csv
import sys

csv.field_size_limit(sys.maxsize)

sample_file = 'csvs/sample_of_interest.csv'
sample_without_arithmetic_file = 'csvs/sample_of_interest_without_arithmetic.csv'
log_file = 'vulnerabilities_log.csv'
log_without_arithmetic_file = 'vulnerabilities_log_without_arithmetic.csv'


def delete_arithmetic_from_sample():
    with open(sample_file, 'r') as file:
        reader = csv.DictReader(file)
        file_read = list(reader)
        fieldnames = reader.fieldnames

    file_to_write = file_read.copy()
    for row in file_to_write:
        new_row = []
        print(f"old row: {row}")
        if row['tag'] != 'no':
            log = row['tag'].split(';')
            for vuln in log:
                if 'arithmetic' in vuln:
                    print(f"removed: {vuln}")
                elif vuln:
                    new_row.append(vuln)

            if len(new_row) == 0:
                row['tag'] = "no"
            else:
                row['tag'] = '; '.join(new_row)
                if not row['tag'].endswith(';'):
                    row['tag'] += ';'

        print(f"new row: {row}")

    with open(sample_without_arithmetic_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_to_write)


def delete_arithmetic_from_log():
    with open(log_file, 'r') as file:
        reader = csv.DictReader(file)
        file_read = list(reader)
        fieldnames = reader.fieldnames

    file_to_write = file_read.copy()
    for row in file_to_write:
        new_row = []
        print(f"old row: {row}")
        if row['Mapped_findings'] != 'no':
            log = row['Mapped_findings'].split(';')
            for vuln in log:
                if 'arithmetic' in vuln:
                    print(f"removed: {vuln}")
                elif vuln:
                    new_row.append(vuln)

            if len(new_row) == 0:
                row['Mapped_findings'] = "no"
            else:
                row['Mapped_findings'] = '; '.join(new_row)
                if not row['Mapped_findings'].endswith(';'):
                    row['Mapped_findings'] += ';'

        print(f"new row: {row}")

    with open(log_without_arithmetic_file, 'w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(file_to_write)


if __name__ == '__main__':
    delete_arithmetic_from_sample()
    delete_arithmetic_from_log()
