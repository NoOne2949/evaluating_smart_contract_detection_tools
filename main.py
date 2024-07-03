from compile import compileContract
from confront_vulnerability import confront_vulnerability
from vulnerability_mapping import process_json_files


def menu():
    print("\n\nMenu:")
    print("1. Compile dataset files")
    print("2. Parse analysis results")
    print("3. Confront tool analysis - WITH ARITHMETIC")
    print("4. Confront tool analysis - WITHOUT ARITHMETIC")
    print("0. Exit")
    choice = input("-: ")

    if choice == '1':
        sol_file_path = 'dataset/'
        compileContract(sol_file_path)
    elif choice == '2':
        results_file_path = 'results/'
        process_json_files(results_file_path)
    elif choice == '3':
        artifacts_file = "csvs/sample_of_interest.csv"
        vulnerability_log = "vulnerabilities_log.csv"
        confront_vulnerability(artifacts_file, vulnerability_log)
    elif choice == '4':
        artifacts_file = "csvs/sample_of_interest_without_arithmetic.csv"
        vulnerability_log = "vulnerabilities_log_without_arithmetic.csv"
        confront_vulnerability(artifacts_file, vulnerability_log)
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid input. Retry...")
    menu()


if __name__ == '__main__':
    menu()
