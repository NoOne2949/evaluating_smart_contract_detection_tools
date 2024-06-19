import csv
import sys

# Increase the field size limit
csv.field_size_limit(sys.maxsize)

# Paths to the datasets
smartbugs_results_path = '../csvs/SmartBugs_Result_Manual_analysis.csv'
smartbugs_curated_path = '../csvs/smartbugs_curated_revised.csv'
zeus_vulnerable_path = '../csvs/ZEUS_manually_tagged_unsafe_contracts_first_revise.csv'
zeus_safe_path = '../csvs/zeusadataset - safe.csv'
output_path = '../csvs/sample_of_interest.csv'

# Initialize the dataset with column headers
merged_dataset = [['label', 'tag', 'contract']]


# Function to read CSV, identify relevant columns, and append rows to the dataset
def read_and_append(filepath, label, tag_column, contract_column):
    with open(filepath, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if row:  # Ensure the row is not empty
                contract = row[contract_column]  # Extract contract address from the specified column
                tag = row.get(tag_column,
                              '')  # Extract the tag from the specified column, default to empty string if not found
                merged_dataset.append([label, tag, contract])


# Read each row from the provided datasets and append to the merged dataset
read_and_append(smartbugs_results_path, 'smartbugs_results', 'labeling', 'address')
read_and_append(smartbugs_curated_path, 'smartbugs_curated', 'Tag', 'name')
read_and_append(zeus_vulnerable_path, 'zeus_vulnerable', 'Tag', 'Address')
read_and_append(zeus_safe_path, 'zeus_safe', 'Tag', 'Address')

# Write the merged dataset to a new CSV file
with open(output_path, mode='w', encoding='utf-8', newline='') as file:
    writer = csv.writer(file)
    writer.writerows(merged_dataset)

print(f"Data merged and saved to {output_path}")
