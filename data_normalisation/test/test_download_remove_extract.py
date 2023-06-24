import os.path
import pymongo
#from urllib import request
import urllib.request # this format to avoid conflict wiht request from pytest fixture
from download_remove_extract import *


@pytest.fixture(params=['../data/objects'])
def remove_json_folder(request):
    folder_path = request.param
    # Call the function to remove the folder content
    if os.path.exists(folder_path):
        shutil.rmtree(folder_path)

def test_remove_json_folder(remove_json_folder):
   assert os.path.exists('../data/objects') is not True


@pytest.fixture(params=['../data'])
def remove_data(request):
    folder_path = request.param
    file_list = os.listdir(folder_path)
    for file_name in file_list:
        file_path = os.path.join(folder_path, file_name)
        if os.path.isfile(file_path):
            os.remove(file_path)
            print(f"Deleted file: {file_path}")

def test_remove_data(remove_data):
    assert len(os.listdir('../data')) == 0


@pytest.fixture(params=['https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e'])
def download_archive(request):
    url = request.param
    if os.path.exists('../data/all_data.gz'):
        os.remove('../data/all_data.gz')
    #request.urlretrieve(url,'../data/all_data.gz')
    urllib.request.urlretrieve(url,'../data/all_data.gz')

def test_download_archive(download_archive):
    assert os.path.exists('../data/all_data.gz')


@pytest.fixture(params=['../data'])
def extract(request):
    file_path = request.param
    input = gzip.GzipFile(file_path + "/all_data.gz", 'rb')
    s = input.read()
    input.close()
    output = open(file_path + "/filename.zip", 'wb')
    output.write(s)
    output.close()
    # unzip .zip
    with zipfile.ZipFile(file_path + "/filename.zip", 'r') as zip_ref:
        zip_ref.extractall(file_path)
    print("unzipped")

def test_extract(extract):
    assert os.path.exists("../data/objects")


@pytest.fixture()
def connect_mongodb():
    # Connection parameters
    mongo_host = 'localhost'
    mongo_port = 27017
    # Create a MongoDB client
    client = pymongo.MongoClient(mongo_host, mongo_port)
    yield client
    # Teardown: Close the MongoDB client connection
    client.close()

def test_connect_mongodb(connect_mongodb):
    database_names = connect_mongodb.list_database_names()
    assert isinstance(database_names, list), "Failed to connect to MongoDB"
