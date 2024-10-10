import pandas as pd

path="sb_curated_gpt_analysis.csv"
# Leggere il CSV
smartbugs_curated_gpt_df = pd.read_csv(path)

# Visualizzare le colonne del DataFrame
print(smartbugs_curated_gpt_df.columns)

# Dizionario delle sostituzioni esatte da effettuare
replace_dict = {
    'bad randomness': 'bad_randomness',
    'access control': 'access_control',
    'time manipulation': 'time_manipulation',
    'unchecked': 'unchecked_low_level_calls',
    'unchecked_low_level_calls_low_level_calls_low_level_calls_low_level_calls': 'unchecked_low_level_calls',
    '\nunchecked_low_level_calls return values for low-level calls': 'unchecked_low_level_calls',
    ' unchecked_low_level_calls return values for low-level calls': 'unchecked_low_level_calls',
    '\n unchecked_low_level_calls return values for low-level calls': 'unchecked_low_level_calls',
    'unchecked_low_level_calls return values for low-level calls': 'unchecked_low_level_calls',
    'short addresses': 'short_addresses',
    'denial of service': 'denial_of_service'

}

# Controllare se la colonna 'Vulnerabilities' esiste
if 'Vulnerabilities' in smartbugs_curated_gpt_df.columns:
    # Iterare su ogni riga e fare la sostituzione manualmente usando at
    for index, value in smartbugs_curated_gpt_df['Vulnerabilities'].items():
        for old_value, new_value in replace_dict.items():
            if old_value in value.lower():  # Se la sottostringa è presente nel valore
                smartbugs_curated_gpt_df.at[index, 'Vulnerabilities'] = value.lower().replace(old_value, new_value)

# Visualizzare i risultati
print(smartbugs_curated_gpt_df['Vulnerabilities'].unique())

# Salvare il DataFrame aggiornato (opzionale)
smartbugs_curated_gpt_df.to_csv(path, index=False)
