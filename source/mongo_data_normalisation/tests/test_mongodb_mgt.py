from mongodb_mgt import *

host = '127.0.0.1'
port = 27017
data_path = "data"
url = "https://diffuseur.datatourisme.fr/webservice/88bb302ae883e577743cce4f0f793282/b09342b4-4114-4c68-9ece-e9bcc36c650e"
mongodb = 'itineraire'
mongo_collection = 'point_interest'
json_files = "test.json"

@pytest.fixture()
def mongoloader():
    mongoloader = MongoDataLoader(host,port,mongodb,mongo_collection,json_files)
    yield mongoloader

# verify connection to mongodb
def test_mongoloader(mongoloader):
    mongoloader.connect_mongodb()
    database_names = mongoloader.list_of_database()
    print("liste database:", database_names)
    assert isinstance(database_names, list), "Failed to connect to MongoDB"
