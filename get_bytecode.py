import requests
import pandas as pd
import time

api_key = 'your_key'


def get_bytecode(contract_address):
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={contract_address}&startblock=0&endblock=99999999&sort=asc&apikey={api_key}'
    response = requests.get(url)
    time.sleep(0.25)

    if response.status_code == 200:
        tx_hash = response.json()['result'][0]['hash']

        url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={tx_hash}&apikey={api_key}'
        response = requests.get(url)

        if response.status_code == 200:
            creator_code = response.json()['result']['input']
            if str(creator_code).startswith("0x"):
                creator_code = creator_code[2:]
                return creator_code
        else:
            print("Error in GET request:", response.status_code)
            return ""
    else:
        print("Errore in GET request:", response.status_code)
        return ""


def save_file(path, content, filename):
    filepath = f"{path}/{filename}"

    try:
        with open(filepath, 'w') as file:
            file.write(content)
        print(f"File saved successfully in: {filepath}")
    except Exception as e:
        print(f"Error while saving file: {e}")


df = pd.read_csv("csvs/sample_of_interest.csv")

for index, row in df.iterrows():
    contract_address = row["contract"]

    if "0x" not in contract_address:
        continue
    bytecode = get_bytecode(contract_address)
    print(bytecode)
    save_folder = "bytecode/sample_of_interest"
    save_file(save_folder, bytecode, contract_address + '.hex')
