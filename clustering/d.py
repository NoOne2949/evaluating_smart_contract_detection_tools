import pandas as pd


# Funzione per modificare il contenuto della colonna 'Tag' nel DataFrame
def modifica_tag(input_file, output_file):
    # Leggi il file CSV in un DataFrame
    df = pd.read_csv(input_file)

    # Modifica il contenuto della colonna 'Tag' se soddisfa la condizione
    df['tag'] = df['tag'].apply(lambda x: 'no' if str(x).strip().lower() == 's' else x)

    # Salva il DataFrame modificato in un nuovo file CSV
    df.to_csv(output_file, index=False)
    print("Modifica completata. Controlla il file '{}'.".format(output_file))


# Esempio di utilizzo
if __name__ == "__main__":
    input_file = '../csvs/sample_of_interest.csv'  # Sostituisci con il tuo file CSV di input
    output_file = input_file  # File CSV di output

    modifica_tag(input_file, output_file)
