import osmnx as ox
from neo4j import GraphDatabase

class Neo4j_Closest_Intersection:

  def __init__(self, uri, user, password):
    self._driver = GraphDatabase.driver(uri, auth=(user, password))

  def close(self):
    self._driver.close()

  def closest_intersection(self):
    with self._driver.session() as session:
        session.write_transaction(self._calcul_closest_intersection)
  
  def _calcul_closest_intersection(self,tx):
    near_intersection_query = ''' 
    CALL apoc.periodic.iterate(
    'MATCH (p:PointOfInterest) WHERE NOT EXISTS ((p)-[:NEAREST_INTERSECTION]->(:Intersection)) RETURN p',
    'CALL {
        WITH p
        MATCH (i:Intersection)
        USING INDEX i:Intersection(location)
        WHERE point.distance(i.location, p.location) < 200

        WITH i
        ORDER BY point.distance(p.location, i.location) ASC 
        LIMIT 1
        RETURN i
    }
    WITH p, i

    MERGE (p)-[r:NEAREST_INTERSECTION]->(i)
    SET r.length = point.distance(p.location, i.location)
    RETURN COUNT(p)',
    {batchSize:1000, parallel:false})
    '''

    #tx.run(near_intersection_query)

    full_text_query = "CREATE FULLTEXT INDEX search_index IF NOT EXISTS FOR (p:PointOfInterest) ON EACH [p.name]"

    results = tx.run(near_intersection_query)
    with self._driver.session() as session:
      results = session.execute_write(lambda tx: tx.run(full_text_query))



