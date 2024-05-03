import os
import csv

# Set the path to your CSV file and folder
csv_file = 'out.csv'
folder_path = 'IMSLP'

# Read the CSV file into a list
with open(csv_file, 'r') as f:
    reader = csv.reader(f)
    file_list = [row[1] for row in reader]

# Get a list of files in the folder
folder_files = os.listdir(folder_path)

# Find files that are in the CSV file but not in the folder
missing_files = [file for file in file_list if file not in folder_files]

# Write the missing files to a new CSV file
with open('missing_files.csv', 'w', newline='') as f:
    writer = csv.writer(f)
    writer.writerow(['File'])  # header row
    for file in missing_files:
        writer.writerow([file])