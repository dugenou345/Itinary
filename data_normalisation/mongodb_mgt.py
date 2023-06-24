import json

import pytest
from pymongo import MongoClient
from decorators import progress_bar

# function to establish connection to Mongodb database, and
@progress_bar
def connect_mongodb(host='127.0.0.1',port=27017):
    client = MongoClient(host=host, port=port)
    return client

@progress_bar
def list_of_database(client):
    print(client.list_database_names())

@progress_bar
def select_database(client,database):
    database = client[database]
    return database

# function to create a new collection in mongodb
@progress_bar
def create_collection(client,database_name, collection):
    database = client[database_name]
    database.create_collection(name=collection)

@progress_bar
def list_collection(client,database_name):
    database = client[database_name]
    collections = database.list_collections()
    for collection in collections:
        print(collection)

@progress_bar
def select_collection(client,database,collection):
    database = client[database]
    collection = database[collection]
    print("selected collection:", collection.name)
    return collection

@progress_bar
def delete_collection(client,database,collection):
    database = client[database]
    collection = database[collection]
    client[database.name][collection.name].drop()

    # Check if the collection exists
    if collection.name in client[database.name].list_collection_names():

        # Delete the collection
        client[database.name][collection.name].drop()
        print(f"The '{collection.name}' collection has been deleted.")
    else:
        print(f"The '{collection.name}' collection does not exist.")


# function to load json files to mongodb
@progress_bar
def load_mongodb(collection, json_files):
    count_insert = 0
    count_json = 0
    for file in json_files:
        with open(file) as f:
            data = json.load(f)
            count_json+=1
            #print(data)
            if(collection.insert_one(data)):
               count_insert+=1
    print(f"Inserted {count_insert} documents in mongodb of {count_json} json files" )

