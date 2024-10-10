import json
import pandas as pd

# Read `sbc_durieux.json`
with open('sbc_durieux.json', 'r') as f_durieux:
    sbc_durieux = json.load(f_durieux)

# Read `sbc_gpt.json`
with open('sbc_gpt.json', 'r') as f_gpt:
    sbc_gpt = json.load(f_gpt)

# Dictionary to store TP, FP, TN, FN counts for each vulnerability
vulnerability_stats = {}

# Iterate over the keys in `sbc_durieux`, treating them as `name`
for name in sbc_durieux.keys():
    print(f"Current name: {name}")

    # Get the associated value from `sbc_durieux`
    durieux_values = sbc_durieux[name]
    print(f"Values in sbc_durieux for '{name}': {durieux_values}")

    # Check if the same `name` exists in `sbc_gpt`
    if name in sbc_gpt:
        gpt_values = sbc_gpt[name]
        print(f"Values in sbc_gpt for '{name}': {gpt_values}")

        # Initialize statistics for each unique vulnerability
        for durieux_value in durieux_values:
            # Strip whitespace and convert to lowercase for comparison
            vulnerability = durieux_value["vulnerability"].strip().lower()

            # Skip "other" and "no" vulnerabilities
            if vulnerability in ["other", "no"]:
                continue

            # Initialize if not already in the dictionary
            if vulnerability not in vulnerability_stats:
                vulnerability_stats[vulnerability] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}

            match_found = False

            for gpt_value in gpt_values:
                # Strip whitespace and compare lines and vulnerability
                gpt_lines = [line for line in gpt_value["lines"]]
                gpt_vulnerability = gpt_value["vulnerability"].strip().lower()

                # Check for matches
                if (durieux_value["lines"] == gpt_lines and
                        vulnerability == gpt_vulnerability):
                    # Count as True Positive
                    vulnerability_stats[vulnerability]["TP"] += 1
                    match_found = True

            if not match_found:
                # If no match found, count as False Negative for Durieux
                vulnerability_stats[vulnerability]["FN"] += 1

    else:
        print(f"Name '{name}' not found in sbc_gpt")

    print("-" * 50)  # Separator for readability

# Calculate False Positives and True Negatives
for gpt_name, gpt_values in sbc_gpt.items():
    for gpt_value in gpt_values:
        vulnerability = gpt_value["vulnerability"].strip().lower()

        # Skip "other" and "no" vulnerabilities
        if vulnerability in ["other", "no"]:
            continue

        # Initialize if not already in the dictionary
        if vulnerability not in vulnerability_stats:
            vulnerability_stats[vulnerability] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}

        # Check if the vulnerability is not found in Durieux values
        found_in_durieux = any(
            gpt_value["lines"] == durieux_value["lines"] and
            vulnerability == durieux_value["vulnerability"].strip().lower()
            for durieux_value in durieux_values
            if gpt_name in sbc_durieux
        )

        if not found_in_durieux:
            # Count as False Positive
            vulnerability_stats[vulnerability]["FP"] += 1

# Prepare data for the CSV
metrics_data = []

# Count False Negatives for Durieux vulnerabilities when GPT vulnerability is "no"
for name in sbc_durieux.keys():
    for durieux_value in sbc_durieux[name]:
        if durieux_value["vulnerability"].strip().lower() == "no":
            # Check if there are no matches in GPT for this Durieux value
            if not any(
                durieux_value["lines"] == gpt_value["lines"] and
                "no" == gpt_value["vulnerability"].strip().lower()
                for gpt_value in sbc_gpt.get(name, [])
            ):
                if "no" not in vulnerability_stats:
                    vulnerability_stats["no"] = {"TP": 0, "FP": 0, "TN": 0, "FN": 0}
                vulnerability_stats["no"]["FN"] += 1

# Calculate and prepare metrics for each vulnerability
for vulnerability, stats in vulnerability_stats.items():
    TP = stats["TP"]
    FP = stats["FP"]
    FN = stats["FN"]
    TN = stats["TN"]  # Assuming TN is known or can be calculated based on your data context

    # Calculate metrics
    precision = TP / (TP + FP) if (TP + FP) > 0 else 0
    recall = TP / (TP + FN) if (TP + FN) > 0 else 0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0
    accuracy = (TP + TN) / (TP + FP + TN + FN) if (TP + FP + TN + FN) > 0 else 0

    # Append metrics to the data list
    metrics_data.append({
        "Vulnerability": vulnerability,
        "TP": TP,
        "FP": FP,
        "TN": TN,
        "FN": FN,
        "Precision": precision,
        "Recall": recall,
        "F1 Score": f1_score,
        "Accuracy": accuracy
    })

# Create a DataFrame and save to CSV
metrics_df = pd.DataFrame(metrics_data)

# Calculate averages for each metric
averages = {
    "Vulnerability": "Average",
    "TP": metrics_df["TP"].mean(),
    "FP": metrics_df["FP"].mean(),
    "TN": metrics_df["TN"].mean(),
    "FN": metrics_df["FN"].mean(),
    "Precision": metrics_df["Precision"].mean(),
    "Recall": metrics_df["Recall"].mean(),
    "F1 Score": metrics_df["F1 Score"].mean(),
    "Accuracy": metrics_df["Accuracy"].mean()
}

# Create a DataFrame for the averages and concatenate
averages_df = pd.DataFrame([averages])
metrics_df = pd.concat([metrics_df, averages_df], ignore_index=True)

# Save the final DataFrame with averages to CSV
metrics_df.to_csv('vulnerability_metrics_with_averages_SBC.csv', index=False)

# Print out the vulnerability statistics
print("Vulnerability Statistics:")
for vulnerability, stats in vulnerability_stats.items():
    print(f"{vulnerability}: {stats}")

print("Metrics saved to 'vulnerability_metrics_with_averages_SBC.csv'")
