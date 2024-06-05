from compile import compileContract
from vulneability_mapping import process_json_files


def menu():
    print("\n\nMenu:")
    print("1. Compile dataset files")
    print("2. Parse analysis results")
    print("0. Exit")
    choice = input("-: ")

    if choice == '1':
        sol_file_path = 'dataset/'
        compileContract(sol_file_path)
        menu()
    elif choice == '2':
        results_file_path = 'results/'
        process_json_files(results_file_path)
        menu()
    elif choice == '0':
        print("Exiting...")
    else:
        print("Invalid input. Retry...")
        menu()


if __name__ == '__main__':
    menu()
