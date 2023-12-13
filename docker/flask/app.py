from flask import Flask, request, jsonify
from neo4j import GraphDatabase
from flask_restx import Api, Resource, fields, marshal


app = Flask(__name__)

# Configuration de la connexion Neo4j
neo4j_uri = "bolt://neo4j-container:7687"
username = "neo4j"
password = "Itinary1"

driver = GraphDatabase.driver(neo4j_uri, auth=(username, password))


def create_poi_transaction(tx, data):
    query = (
        "MATCH (poi:PointOfInterest) "
        "WITH coalesce(max(poi.id), 0) + 1 AS new_id "
        "CREATE (poi:PointOfInterest {id: new_id, name: $name, latitude: $latitude, longitude: $longitude}) "
        "RETURN poi"
    )
    result = tx.run(query, name=data['name'], latitude=data['latitude'], longitude=data['longitude'])
    created_poi = result.single()['poi']
    return {
        'id': created_poi['id'],
        'name': created_poi['name'],
        'latitude': created_poi['latitude'],
        'longitude': created_poi['longitude']
    }

def get_all_poi_transaction(tx):
    query = "MATCH (poi:PointOfInterest) RETURN poi"
    result = tx.run(query)
    return [{'id': record['poi'].id, 'name': record['poi']['name'], 'latitude': record['poi']['latitude'], 'longitude': record['poi']['longitude']} for record in result]


def get_poi_by_id_transaction(tx, id):
    query = (
        "MATCH (poi:PointOfInterest) WHERE id(poi) = $id "
        "RETURN poi"
    )
    result = tx.run(query, id=id)
    record = result.single()
    if record:
        return {
            'id': record['poi'].id,
            'name': record['poi']['name'],
            'latitude': record['poi']['latitude'],
            'longitude': record['poi']['longitude']
        }
    else:
        return None


def update_poi_transaction(tx, id, data):
    query = (
        "MATCH (poi:PointOfInterest) WHERE id(poi) = $id "
        "SET poi.name = $name, poi.latitude = $latitude, poi.longitude = $longitude "
        "RETURN poi"
    )
    result = tx.run(query, id=id, name=data['name'], latitude=data['latitude'], longitude=data['longitude'])
    return result.single()['poi']

def delete_poi_transaction(tx, id):
    query = """
    MATCH (poi:PointOfInterest)
    WHERE id(poi) = $id
    DELETE poi
    """
    tx.run(query, id=id)


# Initialisation de Flask-RESTx et de la documentation Swagger UI
api = Api(app, version='1.0', title='POI API', description='API documentation')

poi_model = api.model('POI', {
    'id': fields.String(readOnly=True, description='The unique identifier of a POI'),
    'name': fields.String(required=True, description='The name of the POI'),
    'latitude': fields.String(required=True, description='The latitude of the POI'),
    'longitude': fields.String(required=True, description='The longitude of the POI'),
})

@api.route('/poi')
class POI(Resource):
    @api.doc(responses={200: 'OK', 500: 'Internal Server Error'})
    @api.marshal_list_with(poi_model)
    def get(self):
        """Get all POIs"""
        with driver.session() as session:
            poi = session.read_transaction(get_all_poi_transaction)
        return poi

    @api.doc(responses={201: 'Created', 400: 'Bad Request', 500: 'Internal Server Error'})
    @api.expect(poi_model)
    @api.marshal_with(poi_model, code=201)
    def post(self):
        """Create a new POI"""
        data = request.json
        with driver.session() as session:
            session.write_transaction(create_poi_transaction, data)
        return data, 201

@api.route('/poi/<int:id>')
@api.param('id', 'The unique identifier of a POI')
@api.response(404, 'POI not found')
class POIItem(Resource):
    @api.doc(responses={200: 'OK', 404: 'POI not found', 500: 'Internal Server Error'})
    @api.marshal_with(poi_model)
    def get(self, id):
        """Get a POI by its ID"""
        with driver.session() as session:
            poi = session.read_transaction(get_poi_by_id_transaction, id)
        if poi is None:
            api.abort(404, "POI not found")
        return poi
    

    @api.doc(responses={200: 'OK', 400: 'Bad Request', 404: 'POI not found', 500: 'Internal Server Error'})
    @api.expect(poi_model)
    @api.marshal_with(poi_model)
    def put(self, id):
        """Update a POI by its ID"""
        data = request.json
        with driver.session() as session:
            poi = session.write_transaction(update_poi_transaction, id, data)
        if poi is None:
            api.abort(404, "POI not found")
        return poi

    @api.doc(responses={200: 'OK', 404: 'POI not found', 500: 'Internal Server Error'})
    @api.response(200, 'OK')
    def delete(self, id):
        """Delete a POI by its ID"""
        with driver.session() as session:
            session.write_transaction(delete_poi_transaction, id)
        return 'POI deleted successfully', 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
