import json
import os

import matplotlib.pyplot as plt
import pandas as pd

zeus_gpt_safe_checked_vulnerabilities = []
sb_gpt_curated_vulnerabilities = []
sb_durieux_curated_vulnerabilities = []
zeus_unsafe_checked_vulnerabilities = []
zeus_safe_checked_vulnerabilities = []
zeus_gpt_unsafe_checked_vulnerabilities = []
true_positives = 0
false_negatives = 0
false_positives = 0
true_negatives = 0
sb_gpt_results_vulnerabilities = []
sb_results_vulnerabilities = []

def analyze_sb_results(vulnerability_in_code, address):
    global sb_results_vulnerabilities, true_negatives
    if ";" in vulnerability_in_code:

        vulns = vulnerability_in_code.strip().split(";")

        for v in vulns:

            if v != '':
                v = v.strip()
                splitted = v.split(':')
                line = splitted[0]
                try:
                    vulnerability = splitted[1]
                    obj = {
                        "line": line,
                        "vulnerability": vulnerability,
                        "address": address
                    }
                except:
                    pass
                sb_results_vulnerabilities.append(obj)

    else:
        if vulnerability_in_code.strip() == 'S':
            obj = {
                "line": 'NO',
                "vulnerability": 'NO',
                "address": address
            }

            sb_results_vulnerabilities.append(obj)


def categorize_correct_analysis(gpt_correct_analysis, path, suptitle):
    arithmetics = 0
    reentrancies = 0
    time_manipulations = 0
    short_addresses = 0
    access_controls = 0
    DOS = 0
    uncheckeds = 0
    front_runnings = 0
    bad_randomnesses = 0
    others = 0

    for analysis in gpt_correct_analysis:
        vulnerability = analysis.get("vulnerability")
        if "arithmetic" in vulnerability:
            arithmetics += 1
        elif "uncheck" in vulnerability:
            uncheckeds += 1
        elif "reentran" in vulnerability:
            reentrancies += 1
        elif "short" in vulnerability:
            short_addresses += 1
        elif "access" in vulnerability:
            access_controls += 1
        elif "time manipulation" in vulnerability:
            time_manipulations += 1
        elif "randomn" in vulnerability:
            bad_randomnesses += 1
        elif "front" in vulnerability:
            front_runnings += 1
        elif "DOS" in vulnerability or "denial" in vulnerability:
            DOS += 1
        else:
            others += 1

    labels = ['Arithmetics', 'Reentrancies', 'Time Manipulations', 'Short Addresses', 'Access Controls', 'DOS',
              'Unchecked Low Level Calls', 'Front Runnings', 'Bad Randomnesses', 'Others']
    counts = [arithmetics, reentrancies, time_manipulations, short_addresses, access_controls, DOS, uncheckeds,
              front_runnings, bad_randomnesses, others]

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, counts, color='skyblue')

    # Add count labels on top of the bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

    plt.xlabel('Vulnerability Type')
    plt.ylabel('Count')
    plt.title('Counts of Correct Detections')
    plt.suptitle(suptitle)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig(path)


def categorize_incorrect_analysis(gpt_incorrect_analysis, path, suptile):
    arithmetics = 0
    reentrancies = 0
    time_manipulations = 0
    short_addresses = 0
    access_controls = 0
    DOS = 0
    uncheckeds = 0
    front_runnings = 0
    bad_randomnesses = 0
    others = 0

    for analysis in gpt_incorrect_analysis:
        vulnerability = analysis.get("vulnerability")
        if "arithmetic" in vulnerability:
            arithmetics += 1
        elif "uncheck" in vulnerability:
            uncheckeds += 1
        elif "reentran" in vulnerability:
            reentrancies += 1
        elif "short" in vulnerability:
            short_addresses += 1
        elif "access" in vulnerability:
            access_controls += 1
        elif "time manipulation" in vulnerability:
            time_manipulations += 1
        elif "randomn" in vulnerability:
            bad_randomnesses += 1
        elif "front" in vulnerability:
            front_runnings += 1
        elif "DOS" in vulnerability or "denial" in vulnerability:
            DOS += 1
        else:
            others += 1

    labels = ['Arithmetics', 'Reentrancies', 'Time Manipulations', 'Short Addresses', 'Access Controls', 'DOS',
              'Unchecked Low Level Calls', 'Front Runnings', 'Bad Randomnesses', 'Others']
    counts = [arithmetics, reentrancies, time_manipulations, short_addresses, access_controls, DOS, uncheckeds,
              front_runnings, bad_randomnesses, others]

    # Create the bar plot
    plt.figure(figsize=(10, 6))
    bars = plt.bar(labels, counts, color='skyblue')

    # Add count labels on top of the bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width() / 2, bar.get_height(), str(count), ha='center', va='bottom')

    plt.xlabel('Vulnerability Type')
    plt.ylabel('Count')
    plt.title('Counts of Incorrect Detections')
    plt.suptitle(suptile)

    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save the plot as an image file
    plt.savefig(path)


def analyze_gpt_analyzed_sb_results(vulnerability_in_code, name):
    global sb_gpt_results_vulnerabilities
    if ";" in vulnerability_in_code:
        vulns = vulnerability_in_code.strip().split(";")

        for v in vulns:
            if v != '':
                v = v.strip()
                splitted = v.split(':')
                line = splitted[0]
                try:
                    vulnerability = splitted[1]
                    obj = {
                        "line": line,
                        "name": name,
                        "vulnerability": vulnerability
                    }
                    sb_gpt_results_vulnerabilities.append(obj)

                except:
                    print(name)


    else:
        obj = {
            "line": 'NO',
            "vulnerability": 'NO',
            "name": name
        }

        sb_gpt_results_vulnerabilities.append(obj)


def analyze_gpt_analyzed_smartbugs_curated(vulnerability_in_code, file_path, name):
    global sb_gpt_curated_vulnerabilities
    if ";" in vulnerability_in_code:
        vulns = vulnerability_in_code.split(";")

        for v in vulns:
            if v != '':
                v = v.strip()

                if(len(v) <= 1):
                    continue

                splitted = v.split(':')
                line = splitted[0]
                try:
                    vulnerability = splitted[1]
                except:
                    print(name)
                    print('aa')
                    print(vulns)
                obj = {
                    "line": line,
                    "name": name,
                    "vulnerability": vulnerability,
                    "file": file_path
                }
                sb_gpt_curated_vulnerabilities.append(obj)
    else:
        obj = {
            "line": 'NO',
            "vulnerability": 'NO',
            "file": file_path,
            "name": name
        }
        sb_gpt_curated_vulnerabilities.append(obj)


def read_and_print_json_properties(json_file_path):

    with open(json_file_path, 'r') as file:
        data = json.load(file)

    for item in data:
        path = item.get("path")
        name = item.get("name")

        vulnerabilities = item.get("vulnerabilities", [])
        for vulnerability in vulnerabilities:
            lines = vulnerability.get("lines")

            category = vulnerability.get("category")
            item_dict = {
                "path": path,
                "lines": lines,
                "vulnerability": category,
                "name": name
            }
            sb_durieux_curated_vulnerabilities.append(item_dict)


def compare_results_on_sb_curated():
    global sb_gpt_curated_vulnerabilities, sb_durieux_curated_vulnerabilities, true_positives, false_positives, false_negatives, true_negatives
    gpt_correct_analysis = []
    gpt_incorrect_analysis = []

    # Inizializziamo i contatori delle metriche
    true_positives = 0
    false_positives = 0
    false_negatives = 0
    true_negatives = 0

    # Dizionari finali per memorizzare i risultati
    results_dict_gpt = {}
    results_dict_item = {}

    # Scorriamo tutte le vulnerabilità GPT (indipendentemente dal risultato del confronto)
    for gpt_item in sb_gpt_curated_vulnerabilities:
        # Crea un elemento per ogni `gpt_item` con "lines" e "vulnerability"
        if gpt_item["name"] not in results_dict_gpt:
            results_dict_gpt[gpt_item["name"]] = []
        if (str(gpt_item["line"])).strip().lower() == 'no':
            gpt_item["line"]="0"
        results_dict_gpt[gpt_item["name"]].append({

            "lines": [int(str(gpt_item["line"]).strip().replace("\'", ""))],
            "vulnerability": gpt_item["vulnerability"]
        })

        # Variabili per verificare se c'è un match corretto o errato
        match_found = False
        false_positive = False

        # Controlla la corrispondenza con le vulnerabilità curate di Durieux
        for item in sb_durieux_curated_vulnerabilities:
            # Controlla se i nomi coincidono
            if gpt_item["name"].lower().strip() == item["name"].lower().strip():
                # Controlla se la vulnerabilità e la linea corrispondono
                if (item["vulnerability"].lower().strip() == gpt_item["vulnerability"].lower().strip() and
                        str(gpt_item["line"]).strip() in [str(line).strip() for line in item["lines"]]):
                    print("trovato")
                    gpt_correct_analysis.append(gpt_item)
                    true_positives += 1
                    match_found = True
                    break  # Esci dal ciclo se troviamo un match corretto
                else:
                    false_positive = True

        # Se non è stato trovato nessun match valido con Durieux, segniamo come falso positivo o negativo
        if match_found:
            continue  # Se è un match corretto, passiamo al prossimo `gpt_item`
        elif false_positive:
            false_positives += 1
            gpt_incorrect_analysis.append(gpt_item)
        else:
            false_negatives += 1
            gpt_incorrect_analysis.append(gpt_item)

    # Creiamo il dizionario results_dict_item per ogni `item` in `sb_durieux_curated_vulnerabilities`
    for item in sb_durieux_curated_vulnerabilities:
        if item["name"] not in results_dict_item:
            results_dict_item[item["name"]] = []

        results_dict_item[item["name"]].append({
            "lines": item["lines"],  # item["lines"] è già una lista
            "vulnerability": item["vulnerability"]
        })

    # Visualizzazione e categorizzazione dei risultati
    categorize_correct_analysis(gpt_correct_analysis, 'correct_gpt_detection_sb_curated.png',
                                'Correct detections on sb_curated')
    categorize_incorrect_analysis(gpt_incorrect_analysis, 'false_positives_gpt_sb_curated.png',
                                  'False Positive Detections on sb_curated')

    # Stampa delle metriche finali
    print(f"True Positives: {true_positives}")
    print(f"False Positives: {false_positives}")
    print(f"False Negatives: {false_negatives}")
    print(f"True Negatives: {true_negatives}")

    # Salva i dizionari come JSON in file separati o stampa il risultato
    with open('sbc_gpt.json', 'w') as f_gpt:
        json.dump(results_dict_gpt, f_gpt, indent=4)

    with open('sb_durieux.json', 'w') as f_item:
        json.dump(results_dict_item, f_item, indent=4)

    # Restituisci i dizionari dei risultati per ulteriore analisi
    return results_dict_gpt, results_dict_item


def compare_results_on_sb_results():
    global sb_gpt_results_vulnerabilities, sb_results_vulnerabilities, false_negatives, true_negatives, true_positives, false_positives
    gpt_correct_analysis = []
    gpt_incorrect_analysis = []
    i = 0
    for item in sb_results_vulnerabilities:
        i += 1

        for gpt_item in sb_gpt_results_vulnerabilities:

            if gpt_item["name"] == item["address"]:
                if item["vulnerability"].strip().lower() in gpt_item["vulnerability"].strip().lower():

                    gpt_correct_analysis.append(gpt_item)
                    if "no" in gpt_item["vulnerability"].strip().lower():
                        if "no" in item["vulnerability"].strip().lower():
                            true_negatives += 1
                        else:
                            false_negatives += 1
                    else:
                        if gpt_item["line"] == item["line"]:
                            true_positives += 1

                else:
                    gpt_incorrect_analysis.append(gpt_item)
                    if "no" in gpt_item["vulnerability"].strip().lower():
                        false_negatives += 1
                    else:
                        false_positives += 1
                        print(item["vulnerability"])
                        print(gpt_item["vulnerability"])
                        print('')


def calculate_metrics(true_positives, true_negatives, false_negatives, false_positives):
    # Calculate accuracy
    accuracy = (true_positives + true_negatives) / (true_positives + true_negatives + false_negatives + false_positives)

    # Calculate precision
    precision = true_positives / (true_positives + false_positives)

    # Calculate recall
    recall = true_positives / (true_positives + false_negatives)

    # Calculate F1-score
    f1_score = 2 * (precision * recall) / (precision + recall)
    print('tp ' + str(true_positives))
    print('tn ' + str(true_negatives))
    print('fp ' + str(false_positives))
    print('fn ' + str(false_negatives))

    return {
        'accuracy': accuracy,
        'precision': precision,
        'recall': recall,
        'f1_score': f1_score
    }

path=os.getcwd()
smartbugs_curated = f"{path}/sb_curated/smartbugs_curated_revised.csv"
smartbugs_curated_df = pd.read_csv(smartbugs_curated)

smartbugs_curated_gpt_df = pd.read_csv(f"{path}/sb_curated/sb_curated_gpt_analysis.csv")
print(smartbugs_curated_gpt_df.keys())
for index, row in smartbugs_curated_gpt_df.iterrows():
    vulnerability_in_code = row["Vulnerabilities"]
    name = row["Path"]
    analyze_gpt_analyzed_smartbugs_curated(vulnerability_in_code.strip(), name, name)

json_file_path = "sb_curated/vulnerabilities.json"
read_and_print_json_properties(json_file_path)

#compare_results_on_sb_curated()




#
sb_results_path =f"{path}/sb_results/sbresult_manual_analysis.csv"
sb_results_df = pd.read_csv(sb_results_path)

gpt_sb_results_path = f"{path}/sb_results/smartbugs_results_gpt_analysis.csv"
gpt_sb_results_df = pd.read_csv(gpt_sb_results_path)

print(gpt_sb_results_df.shape)

gpt_sb_results_path = f"{path}/sb_results/smartbugs_results_gpt_analysis1.csv"
gpt_sb_results_df = pd.read_csv(gpt_sb_results_path)

print(gpt_sb_results_df.shape)

gpt_sb_results_path = f"{path}/sb_results/smartbugs_results_gpt_analysis2.csv"
gpt_sb_results_df = pd.read_csv(gpt_sb_results_path)

print(gpt_sb_results_df.shape)
exit(8)

for index, row in gpt_sb_results_df.iterrows():
    tag = row["Vulnerabilities"]
    address = row["Path"]

    analyze_gpt_analyzed_sb_results(tag, address)

for index, row in sb_results_df.iterrows():
    if row["label"] == 'smartbugs_results':
        tag = row["tag"]
        address = row["contract"]

        analyze_sb_results(tag, address)

compare_results_on_sb_results()


#results = calculate_metrics(true_positives, true_negatives, false_negatives, false_positives)
#print(results)
