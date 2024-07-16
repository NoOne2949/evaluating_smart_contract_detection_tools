import pandas as pd
from sklearn.metrics import cohen_kappa_score

# Read the dataframes (assuming CSV files, adjust as needed)
df1 = pd.read_csv('../smartbugs-results/metadata/vulnerabilities_mapping_rev1.csv')
df2 = pd.read_csv('../smartbugs-results/metadata/vulnerabilities_mapping_rev2.csv')

# Ensure the column names match exactly
df1.columns = df1.columns.str.strip()
df2.columns = df2.columns.str.strip()

# Initialize lists to store comparison results
df1_values = []
df2_values = []

# Iterate over each row in df1
for index, row in df1.iterrows():
    # Find the matching row in df2
    match = df2[(df2['Tools'] == row['Tools']) & (df2['Vulnerability name'] == row['Vulnerability name'])]

    if not match.empty:
        # Get the first matching row (assuming unique matches)
        match = match.iloc[0]

        # Compare the other columns
        for col in df1.columns:
            if col not in ['Tools', 'Vulnerability Name']:
                df1_values.append(str(row[col]).lower())
                df2_values.append(str(match[col]).lower())

# Calculate Cohen's Kappa
kappa = cohen_kappa_score(df1_values, df2_values)

# Print the result
print(f"Cohen's Kappa: {kappa}")
