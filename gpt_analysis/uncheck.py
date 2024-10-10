import pandas as pd

# Leggere il CSV
smartbugs_curated_gpt_df = pd.read_csv("smartbugs_results_gpt_analysis.csv")

# Visualizzare le colonne del DataFrame
print(smartbugs_curated_gpt_df.columns)

# Dizionario delle sostituzioni esatte da effettuare
replace_dict = {
    '; :': '; ',
    ';\n :': ';'
}

# Controllare se la colonna 'Vulnerabilities' esiste
if 'Vulnerabilities' in smartbugs_curated_gpt_df.columns:
    smartbugs_curated_gpt_df['Vulnerabilities'] = smartbugs_curated_gpt_df['Vulnerabilities'].str.replace('; :', '; ',
                                                                                                          regex=False)
    # Iterare su ogni riga e fare la sostituzione manualmente usando at
    for index, value in smartbugs_curated_gpt_df['Vulnerabilities'].items():
        for old_value, new_value in replace_dict.items():
            if old_value in value.lower():  # Se la sottostringa è presente nel valore
                smartbugs_curated_gpt_df.at[index, 'Vulnerabilities'] = value.lower().replace(old_value, new_value)

# Visualizzare i risultati
print(smartbugs_curated_gpt_df['Vulnerabilities'].unique())

# Salvare il DataFrame aggiornato (opzionale)
smartbugs_curated_gpt_df.to_csv("smartbugs_curated_gpt_analysis.csv", index=False)
