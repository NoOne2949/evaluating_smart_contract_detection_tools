from aggregate_artifacts import aggregate_artifacts
from compile import compileContract
from confront_vulnerability import confront_vulnerability
from vulnerability_mapping import process_json_files


def menu():
    print("\n\nMenu:")
    print("1. Compile dataset files")
    print("2. Parse analysis results")
    print("3. Confront tool analysis")
    print("4. Aggregate artifacts csvs")
    print("0. Exit")
    choice = input("-: ")

    if choice == '1':
        sol_file_path = 'dataset/'
        compileContract(sol_file_path)
    elif choice == '2':
        results_file_path = 'results/'
        process_json_files(results_file_path)
    elif choice == '3':
        confront_vulnerability()
    elif choice == '4':
        aggregate_artifacts()
    elif choice == '0':
        print("Exiting...")
        return
    else:
        print("Invalid input. Retry...")
    menu()


if __name__ == '__main__':
    menu()
