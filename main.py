import subprocess
from source.neo4j.import_osmnx_city_country import *


def main():
    # get data from datatourisme, inject in Mongodb, return a filtered json 
    subprocess.call(['python', 'source/data_normalisation/data_normalisation.py'])

    # insert in list of POI filtered in neo4j
    subprocess.call(['python', 'source/neo4j/import_POI_mongo_to_neo4j.py'])

    # generate a geo dataframe of the selected city  
    city = "Paris"
    country = "France"
    network_type = "drive"
    graph = Load_Graph(city,country,network_type)

    # plot the nodes and routes of the selected city
    graph.load_graph_from_place()

if __name__ == '__main__':
    main()