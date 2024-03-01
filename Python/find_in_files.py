import sys
import os
import csv
import argparse

def get_files_in_folder(path, type):
    files = []
    print("Files found:")
    for name in os.listdir(path):
        if name.endswith(type):
            print(name)
            files.append(name)
    return files

def find_text_in_csv(pathname, value1, value2=""):
    '''Search for text in CSV files'''

    total_line_count = 0
    total_num_hits = 0
    file_summaries = []


    with open(str(args.output), 'a') as f:

        files = get_files_in_folder(pathname, args.type)

        # Write to file instead of terminal
        original_stdout = sys.stdout
        sys.stdout = f
        print("----------Starting search------------")

        os.chdir(pathname)

        for filename in files:
            with open(filename) as csv_file:
                print("-----------Start of file----------")
                print("Filename: " + filename)
                csv_reader = csv.reader(csv_file, delimiter=',')
                line_count = 0
                num_hits = 0
                for row in csv_reader:
                    if line_count == 0:
                        print(f'Column names are {", ".join(row)}')
                        line_count += 1
                    else:
                        if value1 in row[1] and value2 in row[1]:
                            num_hits += 1
                            print(f'Line {line_count}: {row}')
                        line_count += 1
                file_summaries.append(f'Processed {line_count} lines in {filename}. Found {num_hits} search results containing "{value1}" and "{value2}"')
                total_line_count += line_count
                total_num_hits += num_hits
            print("-----------End of file----------")
        print('\n'.join(file_summaries))
        print(f'{total_line_count} total lines processed, {total_num_hits} total search results for "{value1}" and "{value2}"')
        print("----------End search------------")
        sys.stdout = original_stdout
        print(f'{total_line_count} total lines processed, {total_num_hits} total search results for "{value1}" and "{value2}"')
    return

#path = r"C:\Users\joelg\Documents\Cases\Alameda County\04964241 - relay access denied"
#type = ".csv"
#searchTerm1 = '166.107.208'
#searchTerm2 = 'reject'

if __name__ == "__main__":
    argv = sys.argv[1:]
    parser = argparse.ArgumentParser()
    # python main.py disconnected 247 -o test.txt -p "C:\Users\joelg\Documents\Cases\Alameda County\04964241 - relay access denied"
    parser.add_argument("-o", "--output", help="Output file", dest="output", default="output.txt")
    parser.add_argument("-p", "--path", help="Working directory", dest="path", default=os.getcwd())
    parser.add_argument("-t", "--type", help="File type", dest="type", default=".csv")
    args, unknown = parser.parse_known_args(argv)

    print(f"Searching for {', '.join(unknown)} in '{args.path}\*{args.type}'")
    find_text_in_csv(args.path, unknown[0], unknown[1])