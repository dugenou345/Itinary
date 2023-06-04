from urllib import request
import gzip
import zipfile
import json
import os
from pymongo import MongoClient

################ Function definition area #####################################

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

# function to establish connection to Mongodb database, and
def connect_mongodb(host,port):
    client = MongoClient(host = host, port = port)
    return client

def list_of_database(client):
    print(client.list_database_names())

def select_database(client,database):
    database = client[database]
    return database

# function to create a new collection in mongodb
def create_collection(client,database_name, collection):
    database = client[database_name]
    database.create_collection(name=collection)

def list_collection(client,database_name):
    database = client[database_name]
    collections = database.list_collections()
    for collection in collections:
        print(collection)

def select_collection(client,database,collection):
    database = client[database]
    collection = database[collection]
    print("selected collection:", collection.name)
    return collection

# function to load json files to mongodb
def load_mongodb(collection, json_files):
    for file in json_files:
        with open(file) as f:
            data = json.load(f)
    print(data)


############################## Main area ########################################

host = '127.0.0.1'

# download json file from datatourisme (.gz)
download_archive(url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e")

# gunzip + unzip archive
extract("all_data.gz")

# recurslively parse folder for json files
json_files = find_json_files('data/objects')

# connect to mongodb
client = connect_mongodb(host,27017)

# list database name from mongodb
list_of_database(client)

# select database in mongodb
database = select_database(client,'itineraire')

# create new collection
create_collection(client,database.name,'point_interest')

# list collection from mongodb (in currently selected database)
list_collection(client,database.name)

# select collection from mongodb database
collection = select_collection(client,'itineraire','point_interest')

# Load json data to mongodb to poi
#load_mongodb(collection, json_files)


