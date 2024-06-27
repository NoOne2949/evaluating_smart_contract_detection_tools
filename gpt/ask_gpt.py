import time

import pandas as pd
import requests

openai_api_key = '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'


def read_contract_and_ask_gpt(path):
    df = pd.read_csv(path)

    gpt_analysis = []

    for index, row in df[:1].iterrows():

        address = row["source"] + '/' + row["path"]
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
    df.to_csv("../../../filtered_datasets/study_context/gpt_analysis/sbr_sample_gpt.csv", index=False)


def ask_gpt(code):
    if openai_api_key is None:
        raise ValueError("OpenAI API key is not set in environment variables.")

    url = "https://api.openai.com/v1/chat/completions"

    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {openai_api_key}"
    }

    data = {
        "model": "gpt-3.5-turbo",
        "messages": [
            {
                "role": "system",
                "content": "You are a smart contract expert, and you're great in finding security vulnerability."
                           " Your role is to find vulnerabilities in the provided smart contracts, please follow the "
                           "DASP Top 10 taxonomy, which encompass Reentrancy, Access Control, Arithmetic, Unchecked "
                           "Return Values For Low Level Calls, Denial of Service, Bad Randomness, Front Running, "
                           "Time Manipulation and Short Addresses."
            },
            {
                "role": "user",
                "content": "Here's the Smart Contract code: "
                           + code + "Please give me only the number of line of code which is vulnerable. "
                                    "Don't you dare to give me any other information or use other vulnerability class."
                                    " You MUST follow this result "
                                    "pattern: line: vulnerability; line: vulnerability; moreover, please follow the "
                                    "DASP Top 10 taxonomy. Remember to follow the provided pattern, do not add other"
                                    " sentences or words, do not use lists, follow the result pattern!"

            }
        ]
    }

    response = requests.post(url, headers=headers, json=data)

    # Check if the request was successful
    if response.status_code == 200:
        print("Response from OpenAI:", response.json())
        print('\n')
        print(response.json()['choices'][0]['message']['content'])
        return response.json()['choices'][0]['message']['content']
    else:
        print("Error:", response.status_code, response.text)


read_contract_and_ask_gpt(
    "../../../filtered_datasets/study_context/sbresult_manual_analysis.csv")
