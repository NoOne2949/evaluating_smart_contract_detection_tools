import csv
import sys

artifacts_file = "csvs/Artifacts.csv"
labelling_data_file = "csvs/Filtered_Manual_analysis.csv"
output_file = "csvs/SmartBugs_Result_Manual_analysis.csv"


def aggregate_artifacts():
    # Increase the field size limit to handle large fields
    csv.field_size_limit(sys.maxsize)

    artifacts_data = {}
    labelling_data = []

    # Read the artifacts data
    with open(artifacts_file, "r") as af:
        reader = csv.DictReader(af)
        for row in reader:
            artifacts_data[row["id"]] = {"address": row["address"], "code": row["code"]}

    # Read the labelling data
    with open(labelling_data_file, "r") as lf:
        reader = csv.DictReader(lf)
        for row in reader:
            labelling_data.append(row)

    # Aggregate the data
    aggregated_data = []
    for row in labelling_data:
        artifact_id = row["artifact_id"]
        if artifact_id in artifacts_data:
            combined_row = row.copy()
            combined_row["address"] = artifacts_data[artifact_id]["address"]
            combined_row["code"] = artifacts_data[artifact_id]["code"]
            aggregated_data.append(combined_row)

    # Define the headers for the output file (all labelling headers + address + code)
    fieldnames = ["address", "code"] + [field for field in labelling_data[0].keys()]

    # Write the aggregated data to the output file
    with open(output_file, "w", newline='') as of:
        writer = csv.DictWriter(of, fieldnames=fieldnames)
        writer.writeheader()
        for row in aggregated_data:
            writer.writerow(row)


# Call the function to execute the aggregation
aggregate_artifacts()
