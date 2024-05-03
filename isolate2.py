import os
import shutil
import random

# Set the input and output folder paths
input_folder = 'IMSLP_images'
output_folder = 'IMSLP_curatedimages'
other_outputfolder = 'IMSLP_curatedimagesextra'

# Create the output folder if it doesn't exist
if not os.path.exists(output_folder):
    os.makedirs(output_folder)

# Get a list of all files in the input folder
files = os.listdir(input_folder)

# Get a list of all files in the output folder
output_files = os.listdir(output_folder)

other_outputfiles = os.listdir(other_outputfolder)

# Create a set of initials that already exist in the output folder
existing_initials = set(file.split('_')[0] for file in other_outputfiles)

# Create a dictionary to store files by initial
files_by_initial = {}

# Iterate over the files in the input folder
for file in files:
    # Extract the initial from the file name
    initial = file.split('_')[0]
    # If the initial doesn't already exist in the output folder, add the file to the dictionary
    if initial not in existing_initials and file not in output_files:
        if initial not in files_by_initial:
            files_by_initial[initial] = [file]
        else:
            files_by_initial[initial].append(file)

# Iterate over the initials
for initial, file_list in files_by_initial.items():
    # Choose a random file from the list
    random_file = random.choice(file_list)
    # Copy the file to the output folder
    shutil.copy(os.path.join(input_folder, random_file), output_folder)
