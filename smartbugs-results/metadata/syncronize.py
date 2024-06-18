import pandas as pd

# Read the CSV files
csv1 = pd.read_csv('vulnerabilities_mapping.csv', engine="python")
csv2 = pd.read_csv('vulnerabilities_mapping_rev2.csv')
tool="conkas"
# Filter rows where Tools is 'slither' in csv1
slither_rows_csv1 = csv1[csv1['Tools'] == tool]

# Check for descriptions in csv2
existing_descriptions_csv2 = csv2[csv2['Tools'] == tool]['Vulnerability name'].tolist()

# Find rows in csv1 where description is not in csv2
new_rows = slither_rows_csv1[~slither_rows_csv1['Vulnerability name'].isin(existing_descriptions_csv2)]

# Set other columns to null and Tools to 'slither'
new_rows.loc[:, new_rows.columns != 'Vulnerability name'] = None
new_rows['Tools'] = tool

# Concatenate the new rows to csv2
csv2 = pd.concat([csv2, new_rows], ignore_index=True)

# Save the updated csv2
csv2.to_csv('vulnerabilities_mapping_rev2.csv', index=False)
