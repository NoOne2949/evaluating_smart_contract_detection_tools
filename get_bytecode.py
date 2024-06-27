import requests
import pandas as pd
import time

# Definisci l'API key e l'indirizzo del contratto
api_key = 'W5QZMBANZBA52HTTK9DFAF2Y9EA3MJDKY9'


def get_bytecode(contract_address):
    # URL dell'API di Etherscan per ottenere il bytecode
    # URL dell'API di Etherscan per ottenere i dettagli della transazione
    # Ottieni l'hash della transazione di creazione del contratto
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
    response = requests.get(url)
    time.sleep(0.25)

    if response.status_code == 200:
        # Estrai l'hash della prima transazione (quella di creazione del contratto)
        tx_hash = response.json()['result'][0]['hash']

        # Ottieni il dettaglio della transazione usando l'hash
        url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            creator_code = response.json()['result']['input']
            if str(creator_code).startswith("0x"):
                creator_code = creator_code[2:]
                return creator_code
        else:
            print("Errore nella richiesta GET:", response.status_code)
            return ""
    else:
        print("Errore nella richiesta GET:", response.status_code)
        return ""


def save_file(path, content, filename):
    # Componi il percorso completo del file
    filepath = f"{path}/{filename}"

    try:
        # Apri il file in modalità scrittura
        with open(filepath, 'w') as file:
            # Scrivi il contenuto nel file
            file.write(content)
        print(f"File salvato correttamente in: {filepath}")
    except Exception as e:
        print(f"Si è verificato un errore durante il salvataggio del file: {e}")


df = pd.read_csv("../../../../filtered_datasets/study_context/smartbugs_curated.csv")

for index, row in df.iterrows():
    contract_address = row["path"]
    contract_address=contract_address.split("/")[2]

    if "0x" not in contract_address:
        continue
    bytecode = get_bytecode(contract_address[:-4])
    print(bytecode)
    save_folder = "../../../../filtered_datasets/study_context/bytecoded/smartbugs_curated"
    save_file(save_folder, bytecode, contract_address + '.hex')
