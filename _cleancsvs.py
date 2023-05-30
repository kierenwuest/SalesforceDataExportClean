import os
import csv
import logging

# This program cleans a folder's set of .csv files, that come from the Salesforce data backup export service, with 'All Objects' checked.
#
# It attempts to:
# 1. Remove irrelevant files (That have no data or identified irrelevant objects that contain data)
# 2. Remove columns from the csv's that have either no data or systemmod stamps.
#
# To run the program, in the terminal, enter "python3 _cleancsvs.py" in the folder of files
# 
# This code was created by Kieren Wuest with Python 3.9.6 and the help of GPT-4.
#
# v0.2 This version handles NULL bytes and replaces them with space characters
# v0.4 This version gives better feedback and fixes History and Summary files.
# v0.5 This version creates a log file called _cleancsvs_log.txt with the outputs of actions for posterity
# v0.6 This version outputs log actions (via use of the 'logging' module) to both termial and cleancsvs_log.txt - Created Github repo

# Configure logging
log_file_path = '_cleancsvs_log.txt'
logging.basicConfig(level=logging.INFO, filename=log_file_path, filemode='a')
logger = logging.getLogger()

def delete_files_with_patterns(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
                # Replace NULL bytes with a space character
                content = csvfile.read().replace('\x00', ' ')
                lines = content.splitlines()
                headers = next(csv.reader([lines[0]]), None)
                data_rows = list(csv.reader(lines[1:]))

            # Check if the file matches the specified patterns or has only one row (header)
            if (("History" in file_name) or
                ("Summary" in file_name) or
                file_name.startswith("TenantSecurity") or
                not data_rows):
                os.remove(file_path)
                logger.info(f"Deleted empty file: {file_name}")
                print(f"Deleted empty file: {file_name}")

def process_csv_file(file_path):
    with open(file_path, newline='', encoding='ISO-8859-1') as csvfile:
        # Replace NULL bytes with a space character
        content = csvfile.read().replace('\x00', ' ')
        lines = content.splitlines()
        headers = next(csv.reader([lines[0]]), None)
        data_rows = list(csv.reader(lines[1:]))

    # Determine which columns to keep
    columns_to_keep = []
    for i, header in enumerate(headers):
        if header in {'CreatedDate', 'CreatedById', 'LastModifiedDate', 'LastModifiedById', 'SystemModstamp'}:
            columns_to_keep.append(False)
        else:
            has_data = any(row[i].strip() for row in data_rows)
            columns_to_keep.append(has_data)

    removed_columns = sum(not keep for keep in columns_to_keep)

    # Write new CSV file without specified columns and columns with no data
    with open(file_path, 'w', newline='', encoding='ISO-8859-1') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([header for header, keep in zip(headers, columns_to_keep) if keep])

        for row in data_rows:
            writer.writerow([cell for cell, keep in zip(row, columns_to_keep) if keep])

    logger.info(f"Processed file: {os.path.basename(file_path)} and removed {removed_columns} empty columns")
    print(f"Processed file: {os.path.basename(file_path)} and removed {removed_columns} empty columns")

def main():
    folder_path = '.'  # The script runs in the folder it is placed in
    delete_files_with_patterns(folder_path)

    for file_name in os.listdir(folder_path):
        if file_name.endswith('.csv'):
            file_path = os.path.join(folder_path, file_name)
            process_csv_file(file_path)

if __name__ == '__main__':
    main()
