from pymongo import MongoClient
from neo4j import GraphDatabase

# Connexion à MongoDB
mongo_client = MongoClient('mongodb://27017:2701/')
mongo_db = mongo_client['Itinary']
mongo_collection = mongo_db['data']

# Connexion à Neo4j
neo4j_uri = "bolt://7687:7687"
neo4j_user = "neo4j"
neo4j_password = "Itinary1"

class Neo4jSessionWrapper:
    def __init__(self):
        self.driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close(self):
        self.driver.close()

    def add_data_to_neo4j(self, data):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, data)

    @staticmethod
    def _create_node(tx, data):
        query = (
            "CREATE (node:DataNode {key: $key, value: $value})"
            "RETURN node"
        )
        result = tx.run(query, key=data['_id'], value=data['field_to_transfer'])
        return result.single()[0]

# Transfert de données de MongoDB à Neo4j
def transfer_data():
    neo4j_session_wrapper = Neo4jSessionWrapper()

    for doc in mongo_collection.find():
        neo4j_session_wrapper.add_data_to_neo4j(doc)

    neo4j_session_wrapper.close()

if __name__ == "__main__":
    transfer_data()
