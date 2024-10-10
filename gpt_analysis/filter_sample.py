import pandas as pd
import os

# Percorsi dei file
input_csv_path = '../sample_of_interest.csv'
output_csv_path = '../sbresult_manual_analysis.csv'

# Leggere il CSV
df = pd.read_csv(input_csv_path)

# Verificare se il file di output esiste già
file_exists = os.path.isfile(output_csv_path)

# Iterare sulle righe del DataFrame
for index, row in df.iterrows():
    label = row["label"]

    # Verificare se la label è 'smartbugs_results'
    if label == 'smartbugs_results':
        # Scrivere questa riga in un nuovo CSV
        with open(output_csv_path, mode='a', newline='') as file:
            if not file_exists:
                row.to_frame().T.to_csv(file, index=False, header=['label', 'tag', 'contract'])
                file_exists = True  # Adesso il file esiste
            else:
                row.to_frame().T.to_csv(file, index=False, header=False)
