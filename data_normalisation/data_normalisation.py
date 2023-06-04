from urllib import request
import gzip
import zipfile
import json
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


# function to establish connection to Mongodb database
def connect_mongodb(host,port):
    client = MongoClient(host = host, port = port)
    print(client.list_database_names())

# function to mongoimport data
def mongo_import():

############################## Main area ########################################

host = '127.0.0.1'
#zu789 = 12.23.45.12
# download json file from datatourisme (.gz)
download_archive(url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e")

# gunzip + unzip archive
extract("all_data.gz")

#normalize json to dataframe
#dict = json.loads("data/objects/0/02/13-022e6234-4c65-3e23-9938-f31ac9ec9bbb.json")
#dict = json.loads(data)
#df2 = json_normalize(dict['technologies'])
#print(df2)

# Load the JSON data
with open("data/objects/0/02/13-022e6234-4c65-3e23-9938-f31ac9ec9bbb.json") as f:
    data = json.load(f)
print(data)

connect_mongodb(host,27017)


#df = pd.read_json("data/objects/0/02/13-022e6234-4c65-3e23-9938-f31ac9ec9bbb.json",orient="rdfs:comment")