import osmnx as ox
from neo4j import GraphDatabase

class Neo4j_Shortest_Path:

  def __init__(self, uri, user, password):
    self._driver = GraphDatabase.driver(uri, auth=(user, password))

  def close(self):
    self._driver.close()

  def shortest_path(self):
    with self._driver.session() as session:
        session.write_transaction(self._calcul_shortest_path)
  
  def _calcul_shortest_path(self,tx):
    shortest_path_query = ''' 
    MATCH (poi_source:PointOfInterest)-[:NEAREST_INTERSECTION]->(source:Intersection)
    WHERE poi_source.name CONTAINS "Timhotel Tour Eiffel"
    MATCH 
      (poi_dest:PointOfInterest)-[:NEAREST_INTERSECTION]->(dest:Intersection) 
    WHERE poi_dest.name CONTAINS "Musée du Louvre"
    CALL apoc.algo.dijkstra(source, dest, "ROAD_SEGMENT", "length") 
    YIELD weight, path
    RETURN *
    //WITH [ x in nodes(path) | {latitude: x.location.latitude, longitude: x.location.longitude}] AS route, weight AS totalDist
    //RETURN *
    '''

    tx.run(shortest_path_query)


