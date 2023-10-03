from neo4j import GraphDatabase

class Neo4j_Importer:
    
    def __init__(self, uri, user, password):
        self._driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self._driver.close()

    def create_constraints_and_indexes(self):
        with self._driver.session() as session:
            session.write_transaction(self._create_constraints)
            session.write_transaction(self._create_indexes)

    def import_nodes(self, nodes_data):
        with self._driver.session() as session:
            session.write_transaction(self._import_nodes, nodes_data)

    def import_relationships(self, rels_data):
        with self._driver.session() as session:
            session.write_transaction(self._import_relationships, rels_data)

    def create_attribute_point_srid(self):
        with self._driver.session() as session:
            session.write_transaction(self._calcul_point_srid)

    def _create_constraints(self, tx):
        # Your Cypher constraint queries here
        constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (i:Intersection) REQUIRE i.osmid IS UNIQUE"
        rel_index_query = "CREATE INDEX IF NOT EXISTS FOR ()-[r:ROAD_SEGMENT]-() ON r.osmids"
        address_constraint_query = "CREATE CONSTRAINT IF NOT EXISTS FOR (a:Address) REQUIRE a.id IS UNIQUE"
        point_index_query = "CREATE POINT INDEX IF NOT EXISTS FOR (i:Intersection) ON i.location"

        tx.run(constraint_query)
        tx.run(rel_index_query)
        tx.run(address_constraint_query)
        tx.run(point_index_query)

    def _create_indexes(self, tx):
        # Additional index creation if needed
        pass

    def _import_nodes(self, tx, nodes_data):
        # Cypher query to import nodes data here
        node_query = '''
            UNWIND $rows AS row
            WITH row WHERE row.osmid IS NOT NULL
            MERGE (i:Intersection {osmid: row.osmid})
                SET i.location = point({latitude: row.y, longitude: row.x}),
                    i.ref = row.ref,
                    i.highway = row.highway,
                    i.street_count = toInteger(row.street_count)
            RETURN COUNT(*) as total
            '''
        
        #tx.run(node_query, rows=nodes_data)
        
        total = 0
        batch = 0
        batch_size = 10000
        rows = nodes_data

        while batch * batch_size < len(rows):
            results = tx.run(node_query, parameters = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')}).data()
            print(results)
            total += results[0]['total']
            batch += 1

    def _import_relationships(self, tx, rels_data):
        # Cypher query to import relationships data here
        rels_query = '''
            UNWIND $rows AS road
            MATCH (u:Intersection {osmid: road.u})
            MATCH (v:Intersection {osmid: road.v})
            MERGE (u)-[r:ROAD_SEGMENT {osmid: road.osmid}]->(v)
                SET r.oneway = road.oneway,
                    r.lanes = road.lanes,
                    r.ref = road.ref,
                    r.name = road.name,
                    r.highway = road.highway,
                    r.max_speed = road.maxspeed,
                    r.length = toFloat(road.length)
            RETURN COUNT(*) AS total
            '''
        #tx.run(rels_query, rows=rels_data)
        
        total = 0
        batch = 0
        batch_size = 10000
        rows = rels_data

        while batch * batch_size < len(rows):
            results = tx.run(rels_query, parameters = {'rows': rows[batch*batch_size:(batch+1)*batch_size].to_dict('records')}).data()
            print(results)
            total += results[0]['total']
            batch += 1


    def _calcul_point_srid(self,tx):
        # Cypher query to create geospatial srid attribute to label PointOfInterest
        geo_srid_query = '''
        MATCH (n:PointOfInterest)
        WHERE n.longitude IS NOT NULL AND n.latitude IS NOT NULL
        SET n.location = point({ x: toFloat(n.longitude), y: toFloat(n.latitude), srid: 4326 })
        '''
        tx.run(geo_srid_query)

