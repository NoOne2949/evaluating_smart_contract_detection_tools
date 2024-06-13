import pandas as pd

# Read the CSV files
csv1 = pd.read_csv('vulnerabilities_mapping_rev1.csv', engine='python')
csv2 = pd.read_csv('vulnerabilities_mapping_rev2.csv')

# Iterate through each row in csv1
for index, row in csv1.iterrows():
    # Check if the value of 'Tools' is 'slither' in both csv1 and csv2
    if row['Tools'] == 'slither':
        vuln_name = row["Vulnerability name"]

        # Get the corresponding row from csv2
        corresponding_row_csv2 = csv2.loc[(csv2['Tools'] == 'slither') & (csv2['Vulnerability name'] == vuln_name)]

        # If there is a corresponding row in csv2
        if not corresponding_row_csv2.empty:

            # Get columns from csv1 with value.lower() == 'true'
            true_columns_csv1 = [column for column, value in row.items() if str(value).lower() == 'true']

            # Get columns from csv2 with value.lower() == 'true'
            true_columns_csv2 = [column for column, value in corresponding_row_csv2.iloc[0].items() if
                                 str(value).lower() == 'true']

            if true_columns_csv2 != true_columns_csv1:
                print('mismatch: ' + vuln_name)
                print("Columns with value 'TRUE' in CSV1:")
                print(true_columns_csv1)
                print()
                print("Columns with value 'TRUE' in CSV2:")
                print(true_columns_csv2)
            else:
                pass
            # No need to continue searching for this row in csv1, so break out of the loop
