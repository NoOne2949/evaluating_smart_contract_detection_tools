import os
import pandas as pd

# Read the CSV file
csv_file = '../csvs/ZEUS_manually_tagged_unsafe_contracts_first_revise.csv'  # Sostituisci con il percorso del tuo file CSV
csv_data = pd.read_csv(csv_file)
count=0
# Directory to check
base_directory = 'mythril'
if not os.path.exists(base_directory):
    print(f"The directory {base_directory} does not exist.")
else:
    # Store all directory names for faster lookup
    directory_names = []
    for root, dirs, files in os.walk(base_directory):
        directory_names.extend(dirs)

    # Iterate over each row in the CSV
    for index, row in csv_data.iterrows():
        # Extract the Address value and append .sol extension
        address = row['Address']
        address_folder_name = f"{address}.sol".strip()

        # Check if Address is a name of any folder in /mythril
        if address_folder_name in directory_names:
            print(f"Address '{address_folder_name}' found as a folder in {base_directory}")
            count+=1
        else:
            print(f"Address '{address_folder_name}' not found as a folder in {base_directory}")


print(count)