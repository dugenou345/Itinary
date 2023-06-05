import json
from pymongo import MongoClient
from bson import ObjectId
from my_projection import my_projection

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


def export_filtered_data_json(client,database,collection):
    database = client[database]
    collection = database[collection]

    # search for mongodb and extract result based on my_projection
    result = collection.find({}, my_projection)
    # Convert the result to a list of dictionaries
    documents = list(result)
    # Define the file path for exporting the JSON data
    file_path = "data_result/result_filtered.json"
    # Write the documents to the JSON file using the custom encoder
    with open(file_path, "w") as file:
        json.dump(documents, file, cls=MongoEncoder)

# Custom JSON encoder to handle MongoDB ObjectId
class MongoEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ObjectId):
            return str(obj)
        return super().default(obj)
