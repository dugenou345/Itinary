import pandas as pd

from download_remove_extract import *
from mongodb_mgt import *
from export_mongodb_2_json import *
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
#export_json = Export_Json(host,port,mongodb,mongo_collection,json_files)

# connect to mongodb
#export_json.connect_mongodb()

# Export filtered data from mongodb according to my_projection.py filter
#export_json.mongodb_projection()


"""

# instanciation json pandas cleaner
json_pandas_cleaner = Json_Pandas_Cleaner(json_file)

# load json file in pandas
df = json_pandas_cleaner.load_pandas()

pd.set_option('display.max_columns', None)

#print(df)

# flatten list
df['new_email'] = json_pandas_cleaner.flatten_list(df,'email')
df['new_shortdescription'] = json_pandas_cleaner.flatten_list(df,'shortdescription')
#df['new_streetaddress'] = [val for sub_sublist in df['streetaddress'] for sublist in sub_sublist for val in sublist]
df['new_postalcode'] = [val for sub_sublist in df['postalcode'] for sublist in sub_sublist for val in sublist]
df['new_department'] = [val for sub_sublist in df['department'] for sublist in sub_sublist for val in sublist]
df['new_region'] = [val for sub_sublist in df['region'] for sublist in sub_sublist for val in sublist]
df['new_maxprice'] = json_pandas_cleaner.flatten_list(df,'maxprice')
df['new_minprice'] = json_pandas_cleaner.flatten_list(df,'minprice')
df['new_pricecurrency'] = json_pandas_cleaner.flatten_list(df,'pricecurrency')
df['new_review'] = json_pandas_cleaner.flatten_list(df,'review')
df['new_label'] = json_pandas_cleaner.flatten_list(df,'label')

# concat string ['Vélo', 'Vélo à assistance électrique, VAE'] ----> ['Vélo, Vélo à assistance électrique, VAE']
#df['new_label'] = json_pandas_cleaner.concat_string(df,'label')

#df['new_label'] = json_pandas_cleaner.concat_string(df,'label')

# convert list to string
df['new_email'] = [','.join(map(str, l)) for l in df['new_email']]
df['new_shortdescription'] = [','.join(map(str, l)) for l in df['new_shortdescription']]
df['new_postalcode'] = [','.join(map(str, l)) for l in df['new_postalcode']]
df['new_department'] = [','.join(map(str, l)) for l in df['new_department']]
df['new_region'] = [','.join(map(str, l)) for l in df['new_region']]
df['new_maxprice'] = [','.join(map(str, l)) for l in df['new_maxprice']]
df['new_minprice'] = [','.join(map(str, l)) for l in df['new_minprice']]
df['new_pricecurrency'] = [','.join(map(str, l)) for l in df['new_pricecurrency']]
df['new_review'] = [','.join(map(str, l)) for l in df['new_review']]
df['new_latitude'] = [','.join(map(str, l)) for l in df['latitude']]
df['new_longitude'] = [','.join(map(str, l)) for l in df['longitude']]

#print('label:', result)
print(df)
#print("type:",type(df['label'][83]))

#print(df_converted_str)
#print(df_removed_bracket)

"""