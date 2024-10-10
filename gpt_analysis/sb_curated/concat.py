import pandas as pd

# Leggi i due file CSV
df1 = pd.read_csv("sb_curated_gpt_analysis.csv")
df2 = pd.read_csv("sb_curated_gpt_analysis2.csv")

# Concatena i due DataFrame
df_combined = pd.concat([df1, df2], ignore_index=True)

# Salva il risultato in un nuovo file CSV chiamato '3.csv'
df_combined.to_csv("3.csv", index=False)
print(df_combined.shape)
print("File concatenato e salvato come 3.csv")
