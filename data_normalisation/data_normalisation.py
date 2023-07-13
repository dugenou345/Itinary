import pandas as pd
from download_remove_extract import *
from mongodb_mgt import *
from extract_data_mongodb import *
from data_cleansing import *
import numpy as np
from pprint import pprint

host = '127.0.0.1'
port = 27017
data_path = "data"
url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e"
#url = "https://diffuseur.datatourisme.fr/webservice/5ee791b415ae416d146156e7a5dc3f2c/b09342b4-4114-4c68-9ece-e9bcc36c650e"
#url = "https://diffuseur.datatourisme.fr/webservice/4e966c92255e3a0a5cb01f6957d69a74/b09342b4-4114-4c68-9ece-e9bcc36c650e"
mongodb = 'itineraire'
mongo_collection = 'point_interest'
json_file = './data_result/result_filtered.json'

#instanciation object DataDownloader
datadownloader = DataDownloader(host,port,data_path,url)

# Remove previous json data
datadownloader.remove_json_folder()

# Remove previous file in data folder
datadownloader.remove_data_files()

#download json file from datatourisme (.gz)
datadownloader.download_archive()

# gunzip + unzip archive
#extract(file_path = 'data')
datadownloader.extract()

# recurslively parse folder for json files
#json_files = find_json_files('data/objects')
json_files = datadownloader.find_json_files()

# create mongoloader object
mongoloader = MongoDataLoader(host,port,mongodb,mongo_collection,json_files)

# connect to mongodb
mongoloader.connect_mongodb()

# list database name from mongodb
mongoloader.list_of_database()

# select database in mongodb
mongoloader.select_database()

#delete previous collection itineraire
mongoloader.delete_collection()

# create a new collection itineraire
mongoloader.create_collection()

# list collection from mongodb (in currently selected database)
mongoloader.list_collection()

# Load json data to mongodb database itineraire in collection point_of_interest
mongoloader.load_mongodb()

#query poi in itinerary collection in mongodb
mongoloader.list_poi()

# JSON exporter instanciation
extract_data_mongodb = Extract_data_mongodb(host,port,mongodb,mongo_collection,json_files)

# connect to mongodb
extract_data_mongodb.connect_mongodb()

# Extract filtered data from mongodb according to my_projection.py filter
extract_data_mongodb.mongodb_projection()

# Export filtered data from mongodb according to my_projection.py filter
extract_data_mongodb.mongodb_export_2_json

# instanciation json pandas cleaner
json_pandas_cleaner = Json_Pandas_Cleaner(json_file)

# load json file in pandas
df = json_pandas_cleaner.load_pandas()
pd.set_option('display.max_columns', None)
print(df)

#check if df contains Nan
json_pandas_cleaner.nan_check_pandas()

#check if df contains duplicates
json_pandas_cleaner.number_duplicates()