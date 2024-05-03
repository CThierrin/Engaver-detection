import os
import requests
import concurrent.futures
import pandas as pd

# List of filenames
filenames = pd.read_csv('missing_files.csv')["File"].to_list()

#filenames = pd.read_csv('out.csv')
 # replace with your list of 1000 filenames

# IMSLP base URL
base_url = "https://imslp.org/tools/getfile/"

# Create a directory to store the downloaded files
download_dir = "IMSLP"
if not os.path.exists(download_dir):
    os.makedirs(download_dir)

def download_file(filename):
    url = base_url + filename
    response = requests.get(url, stream=True)
    if response.status_code == 200:
        with open(os.path.join(download_dir, filename), "wb") as f:
            for chunk in response.iter_content(1024):
                f.write(chunk)
        print(f"Downloaded {filename}")
    else:
        print(f"Error downloading {filename}: {response.status_code}")

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
    futures = [executor.submit(download_file, filename) for filename in filenames]
    for future in concurrent.futures.as_completed(futures):
        future.result()