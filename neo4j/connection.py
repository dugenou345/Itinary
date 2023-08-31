from pymongo import MongoClient
from neo4j import GraphDatabase
from bson.objectid import ObjectId

# Connexion à MongoDB
mongo_client = MongoClient('mongodb://localhost:27017/')
mongo_db = mongo_client['itineraire']
mongo_collection = mongo_db['point_interest']

# Connexion à Neo4j
neo4j_uri = "bolt://localhost:7687"
neo4j_user = "neo4j"
neo4j_password = "Itinary1"

class Neo4jSessionWrapper:
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))
    
    def close(self):
        self._driver.close()
    
    def add_data_to_neo4j(self, data):
        with self._driver.session() as session:
            existing_node = self._find_node_by_id(session, data['_id'])
            if not existing_node:
                self._create_node(session, data)
    
    @staticmethod
    def _find_node_by_id(session, node_id):
        query = "MATCH (n:YourNodeLabel {id: $id}) RETURN n LIMIT 1"
        result = session.run(query, id=str(node_id))
        return result.single()

    @staticmethod
    def _create_node(session, data):
        query = (
            "CREATE (n:PointOfInterest {"
            "id: $id, name: $name, latitude: $latitude, longitude: $longitude})"
        )
        
        is_located_at = data.get('isLocatedAt', [{}])[0]
        latitude = is_located_at.get('schema:geo', {}).get('schema:latitude')
        longitude = is_located_at.get('schema:geo', {}).get('schema:longitude')
        
        session.run(query, id=str(data['_id']), name=data['rdfs:label']['fr'][0], 
                    latitude=latitude, 
                    longitude=longitude
                   )

# Récupérer les données depuis MongoDB
docs = mongo_collection.find({})

# Initialiser la connexion Neo4j
neo4j_session_wrapper = Neo4jSessionWrapper(neo4j_uri, neo4j_user, neo4j_password)

# Transférer les données de MongoDB vers Neo4j
for doc in docs:
    neo4j_session_wrapper.add_data_to_neo4j(doc)

# Fermer la connexion Neo4j
neo4j_session_wrapper.close()