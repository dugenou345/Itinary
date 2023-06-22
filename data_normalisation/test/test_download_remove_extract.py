import os.path
from download_remove_extract import *


def test_remove_json_folder():
    folder_path = "../data/objects"
    # Call the function to remove the folder content
    if os.path.exists(folder_path):
        remove_json_folder(folder_path)
        assert os.path.exists(folder_path) is not True


def test_remove_data_files():
    remove_data_files('../data')
    assert len(os.listdir('../data')) == 0


def test_download_archive():
    assert os.path.exists('../data') == True
    if os.path.exists('../data/all_data.gz'):
        os.remove('../data/all_data.gz')
    # download_archive(url="https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e")
    download_archive(
        url="https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e",
        file_path='../data/all_data.gz')
    assert os.path.exists('../data/all_data.gz')


def test_extract(file_path = '../data/'):
    #extract("../data/all_data.gz")
    extract(file_path)
    assert os.path.exists(file_path+"/objects")
