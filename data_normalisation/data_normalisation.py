from urllib import request
import gzip
import zipfile
import pandas as pd
import json
from pandas import json_normalize

def download_archive(url):
    request.urlretrieve(url, "data/all_data.gz")

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


# download json file from datatourisme (.gz)
download_archive(url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e")

# gunzip + unzip archive
extract("all_data.gz")
