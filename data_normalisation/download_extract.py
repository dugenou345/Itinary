from urllib import request
import gzip
import zipfile
import os

# function to download archive from a Url in parameter
def download_archive(url):
    request.urlretrieve(url, "data/all_data.gz")

# function to gunzip and unzip an archive
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

def find_json_files(folder_path):
    json_files = []

    # Iterate over all files and folders in the given folder path
    for root, dirs, files in os.walk(folder_path):
        for file in files:
        # Check if the file has a .json extension
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                json_files.append(file_path)
        print(json_files)
    return json_files