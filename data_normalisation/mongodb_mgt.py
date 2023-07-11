import json
import pytest
from pymongo import MongoClient
from decorators import progress_bar
from pprint import pprint

class MongoDataLoader:
    def __init__(self,host,port,mongodb,mongo_collection,json_files):
        self.host = host
        self.port = port
        self.mongodb = mongodb  # database itineraire
        self.mongo_collection = mongo_collection  #collecton "point of interest
        self.json_files = json_files

    # function to establish connection to Mongodb database
    @progress_bar
    def connect_mongodb(self):
        self.client = MongoClient(self.host, self.port)

    @progress_bar
    def list_of_database(self):
        database_names = self.client.list_database_names()
        print(database_names)
        return database_names

# MongoDB database selection
    @progress_bar
    def select_database(self):
        self.mydb = self.client[self.mongodb]

# Mongodb delete collection itineraire if exist
    @progress_bar
    def delete_collection(self):
        # Check if the collection exists
        if self.mongo_collection in self.client[self.mongodb].list_collection_names():
            # Delete the collection
            self.client[self.mongodb][self.mongo_collection].drop()
            print(f"The '{self.mongo_collection}' collection has been deleted.")
        else:
            print(f"The '{self.connect_mongodb}' collection does not exist.")

    # function to create a new collection in mongodb
    @progress_bar
    def create_collection(self):
        self.mydb.create_collection(self.mongo_collection)

    @progress_bar
    def list_collection(self):
        # Get the list of collection names
        collection_names = [name for name in self.client[self.mongodb].list_collection_names()]
        # Print the collection names
        print(f"List of collection(s) in database {self.mongodb}: {collection_names}")

# function to load json files to mongodb
    @progress_bar
    def load_mongodb(self):
        for file in self.json_files:
            with open(file) as f:
                data = json.load(f)
                self.client[self.mongodb][self.mongo_collection].insert_one(data)

        # stats on database
        result = self.client[self.mongodb].command("dbStats")
        print(result)

    @progress_bar
    def list_poi(self):
        all_documents = self.client[self.mongodb][self.mongo_collection]
        for i in list(all_documents.find({},{"dc:identifier": 1, "hasTheme.rdfs:label.fr": 1})):
            print(i)
