import time
import pandas as pd
import requests
import json

openai_api_key = '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'


def read_contract_and_ask_gpt(path):
    df = pd.read_csv(path)

    gpt_analysis = []

    for index, row in df[:2].iterrows():

        address = row["name"]
        source_code = row["source_code"]
        start_time = time.time()
        vulnerabilities = ask_gpt(source_code)
        end_time = time.time()

        if vulnerabilities is not None:
            passed_time = end_time - start_time

            found_vulns = {"Path": address,
                           "Vulnerabilities": vulnerabilities,
                           "Time": passed_time}
            gpt_analysis.append(found_vulns)
    df = pd.DataFrame(gpt_analysis)
    path = "../gpt_analysis/sb_curated/sb_curated_gpt_analysis_final.csv"
    df.to_csv(path, index=False)


def ask_gpt(code):
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }
    print(code)

    data = {
        "model": "gpt-4",
        "temperature": 0,
        "messages": [
            {
                "role": "system",
                "content": (
                    "You are an expert in smart contract security, specializing in identifying vulnerabilities. "
                    "Use the DASP Top 10 taxonomy: Reentrancy, Access Control, Arithmetic Issues, "
                    "Unchecked Return Values, Denial of Service, Bad Randomness, Front Running, Time Manipulation, "
                    "and Short Addresses."
                )
            },
            {
                "role": "user",
                "content": (
                    f"Analyze the following smart contract code: {code}. "
                    "List only the line numbers and the type of vulnerability in this format: "
                    "'34: Reentrancy; 41: Access Control;'. If no vulnerabilities are found, respond with 'no'. "
                    "If uncertain between two vulnerabilities, list both. "
                    "Do not include any extra information or use any other vulnerability classes outside of the DASP taxonomy. "
                    "Follow the format exactly as instructed."
                )
            }
        ]
    }

    print(data["messages"])

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response from OpenAI:", response.json())
        print('\n')
        print(response.json()['choices'][0]['message']['content'])
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)


# Esegui la funzione con il file specificato
read_contract_and_ask_gpt("../gpt_analysis/sb_curated/smartbugs_curated_revised.csv")
