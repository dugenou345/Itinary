import subprocess
from source.neo4j.import_osmnx_city_country import *
from source.neo4j.neo4j_importer import *

uri = "bolt://localhost:7687"
user = "neo4j"
password = "Itinary1"

def main():
    # get data from datatourisme, inject in Mongodb, return a filtered json 
    subprocess.call(['python', 'source/data_normalisation/data_normalisation.py'])

    # insert in list of POI filtered in neo4j
    subprocess.call(['python', 'source/neo4j/import_POI_mongo_to_neo4j.py'])

    # generate a geo dataframe of the selected city  
    city = "Paris"
    #city = "San Mateo"
    country = "France"
    #country = "USA"
    network_type = "drive"
    graph = Load_Graph(city,country,network_type)

    # plot the nodes and routes of the selected city
    graph.load_graph_from_place()

    #Generate geo dataframe nodes and relashionships
    gdf_nodes, gdf_relationships = graph.load_geo_dataframe()

    # Create an instance of Neo4jImporter
    neo4j_importer = Neo4j_Importer(uri, user, password)
    
    # Create constraints and indexes
    neo4j_importer.create_constraints_and_indexes()

    #print(gdf_nodes.head())
    print(gdf_nodes.drop(columns=['geometry']))
    neo4j_importer.import_nodes(gdf_nodes.drop(columns=['geometry']))
    
    print(gdf_relationships.drop(columns=['geometry']))
    neo4j_importer.import_relationships(gdf_relationships.drop(columns=['geometry']))

    neo4j_importer.create_attribute_point_srid()



if __name__ == '__main__':
    main()