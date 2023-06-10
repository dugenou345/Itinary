from urllib import request
import gzip
import zipfile
import os
import shutil
from decorators import progress_bar

@progress_bar
def remove_local_json_folder(data):
    # Specify the path of the folder to be removed
    folder_path = data

    #print("removing previous json files")
        # Remove the folder and its contents
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        print(f"Subfolder '{folder_path}' does not exist.")


# function to download archive from a Url in parameter
@progress_bar
def download_archive(url):
    print("downloading json files from datatoursime")
    request.urlretrieve(url, "data/all_data.gz")

# function to gunzip and unzip an archive
@progress_bar
def extract(filename):
    # gunzip .gz
    input = gzip.GzipFile("data/"+filename, 'rb')
    s = input.read()
    input.close()

    output = open("data/filename.zip", 'wb')
    output.write(s)
    output.close()

    # unzip .zip
    with zipfile.ZipFile("data/filename.zip", 'r') as zip_ref:
        zip_ref.extractall("data")

    print("unzipped")

@progress_bar
def find_json_files(folder_path):
    json_files = []

    # Iterate over all files and folders in the given folder path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
        # Check if the file has a .json extension
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                json_files.append(file_path)
        #print(json_files)
    return json_files