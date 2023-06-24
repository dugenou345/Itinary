from urllib import request
import gzip
import zipfile
import os
import shutil

import pytest

from decorators import progress_bar


@progress_bar
def remove_json_folder(json_path):
    # Specify the path of the folder to be removed
    folder_path = json_path
    #print("removing previous json files")
        # Remove the folder and its contents
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)
    else:
        print(f"Subfolder '{folder_path}' does not exist.")


@progress_bar
#@pytest.fixture(params=['./data'])
def remove_data_files(data_path):
    folder_path = data_path
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")


# function to download archive from a Url in parameter
@progress_bar
def download_archive(url,file_path):
    print("downloading json files from datatourisme")
    request.urlretrieve(url,file_path)

# function to gunzip and unzip an archive
@progress_bar
def extract(file_path):
    # gunzip .gz
    input = gzip.GzipFile(file_path+"/all_data.gz", 'rb')
    s = input.read()
    input.close()

    output = open(file_path+"/filename.zip", 'wb')
    output.write(s)
    output.close()

    # unzip .zip
    with zipfile.ZipFile(file_path+"/filename.zip", 'r') as zip_ref:
        zip_ref.extractall(file_path)

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