import pandas as pd
import os

# Percorsi dei file CSV
gpt_sbr_path = 'smartbugs_results.csv'
sbresult_manual_analysis_path = '../sbresult_manual_analysis.csv'
output_csv_path = 'filtered_gpt_sbr.csv'

# Leggere i file CSV
gpt_sbr_df = pd.read_csv(gpt_sbr_path)
sbresult_manual_analysis_df = pd.read_csv(sbresult_manual_analysis_path)

# Ottenere i valori della colonna 'contract' da sbresult_manual_analysis_df
contract_values = sbresult_manual_analysis_df['contract'].tolist()

# Verificare se il file di output esiste già
file_exists = os.path.isfile(output_csv_path)

# Iterare sulle righe di gpt_sbr_df
for index, row in gpt_sbr_df.iterrows():
    path_value = row['Path']

    # Se il valore di 'Path' è in contract_values, scrivere la riga nel nuovo CSV
    if path_value in contract_values:
        with open(output_csv_path, mode='a', newline='') as file:
            if not file_exists:
                row.to_frame().T.to_csv(file, index=False, header=True)
                file_exists = True  # Adesso il file esiste
            else:
                row.to_frame().T.to_csv(file, index=False, header=False)
