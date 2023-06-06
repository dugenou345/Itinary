import json
from pymongo import MongoClient


# function to establish connection to Mongodb database, and
def connect_mongodb(host,port):
    client = MongoClient(host=host, port=port)
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
    count_insert = 0
    count_json = 0
    for file in json_files:
        with open(file) as f:
            data = json.load(f)
            count_json+=1
            print(data)
            if(collection.insert_one(data)):
               count_insert+=1
    print(f"Inserted {count_insert} documents in mongodb of {count_json} json files" )

