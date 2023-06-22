from download_remove_extract import *
from mongodb_mgt import *
from export_mongodb_2_json import *
import pytest

host = '127.0.0.1'
port = 27017
data_path = "data"
json_path = "data/objects"

# Remove previous json data
remove_json_folder(json_path)
# Remove previous file in data folder
remove_data_files(data_path)

#download json file from datatourisme (.gz)
download_archive(url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e",file_path = 'data/all_data.gz')
#download_archive('data/all_data.gz',url = "https://diffuseur.datatourisme.fr/webservice/5ee791b415ae416d146156e7a5dc3f2c/b09342b4-4114-4c68-9ece-e9bcc36c650e")

# gunzip + unzip archive
#extract("all_data.gz")
#extract(file_path = 'data/all_data.gz')
extract(file_path = 'data')
# recurslively parse folder for json files
json_files = find_json_files('data/objects')

# connect to mongodb
client = connect_mongodb(host,port)

# list database name from mongodb
list_of_database(client)

# select database in mongodb
database = select_database(client,'itineraire')

#delete previous collection
delete_collection(client,database.name,'point_interest')

# create new collection
create_collection(client,database.name,'point_interest')

# list collection from mongodb (in currently selected database)
list_collection(client,database.name)

# select collection from mongodb database
collection = select_collection(client,database.name,'point_interest')

# Load json data to mongodb to poi
load_mongodb(collection, json_files)

#export relevant data in database itineraire / collection point_interest
export_filtered_data_json(client,database.name,'point_interest')


