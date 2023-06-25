import os.path
import pymongo
import pytest
#from urllib import request
import urllib.request # this format to avoid conflict with request from pytest fixture
from download_remove_extract import *

host = '127.0.0.1'
port = 27017
data_path = "data"
url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e"

@pytest.fixture
def data_downloader(tmpdir):
    data_path = tmpdir.mkdir("data")
    downloader = DataDownloader(host,port,str(data_path),url)
    yield downloader


def test_data_downloader(data_downloader):
    data_downloader.remove_json_folder()
    assert os.path.exists(data_downloader.data_path+'/objects') is not True

    data_downloader.remove_data_files()
    assert len(os.listdir(data_downloader.data_path)) == 0

    data_downloader.download_archive()
    assert os.path.exists(data_downloader.data_path + '/all_data.gz')

    data_downloader.extract()
    assert os.path.exists(data_downloader.data_path+"/objects")

""""
def test_remove_data_files(data_downloader):
    data_downloader.remove_data_files()
    assert len(os.listdir(data_downloader.data_path)) == 0
"""

""""
def test_download_archive(data_downloader):
    data_downloader.download_archive()
    assert os.path.exists(data_downloader.data_path+'/all_data.gz')
"""

""""
def test_extract(data_downloader):
    data_downloader.extract()
    #assert os.path.exists(data_downloader.data_path+"/objects")
"""

"""
    url = "https://example.com/data.gz"
    file_path = str(data_downloader.data_path.join("all_data.gz"))

    data_downloader.download_archive(url, file_path)
    data_downloader.extract(str(data_downloader.data_path))
    json_files = data_downloader.find_json_files()

    # Perform assertions or further actions based on json_files
    """

# Run the test
#test_data_download()

"""
@pytest.fixture(params=['../data/objects'])
def remove_json_folder(request):
    json_path = request.param
    # Call the function to remove the folder content
    if os.path.exists(json_path):
        shutil.rmtree(json_path)

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

"""