from urllib import request
import gzip
import zipfile
import os
import shutil
from decorators import progress_bar

class DataDownloader:
    def __init__(self, host, port, data_path, url):
        self.host = host
        self.port = port
        self.data_path = data_path
        self.url = url

    @progress_bar
    def remove_json_folder(self):
        # Specify the path of the folder to be removed
        json_path = self.data_path+"/objects"
        #print("removing previous json files")
            # Remove the folder and its contents
        if os.path.exists(json_path):
            shutil.rmtree(json_path)
        else:
            print(f"Subfolder '{json_path}' does not exist.")


    @progress_bar
    def remove_data_files(self):
        folder_path = self.data_path

        file_list = os.listdir(folder_path)
        for file_name in file_list:
            file_path = os.path.join(folder_path, file_name)
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")


    # function to download archive from a Url in parameter
    @progress_bar
    def download_archive(self):
        url = self.url
        file_path = self.data_path+'/all_data.gz'
        print("downloading json files from datatourisme")
        request.urlretrieve(url,file_path)

    # function to gunzip and unzip an archive
    @progress_bar
    def extract(self):
        file_path = self.data_path
        # gunzip .gz
        input = gzip.GzipFile(file_path+"/all_data.gz", 'rb')
        s = input.read()
        input.close()

        output = open(file_path+"/filename.zip", 'wb')
        output.write(s)
        output.close()

        # unzip .zip
        with zipfile.ZipFile(file_path+"/filename.zip", 'r') as zip_ref:
            zip_ref.extractall(file_path)
        print("unzipped")

    @progress_bar
    def find_json_files(self):
        folder_path = self.data_path+'/objects'
        json_files = []

        # Iterate over all files and folders in the given folder path
        for root, dirs, files in os.walk(folder_path):
            for file in files:
            # Check if the file has a .json extension
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    json_files.append(file_path)
            #print(json_files)
        return json_files