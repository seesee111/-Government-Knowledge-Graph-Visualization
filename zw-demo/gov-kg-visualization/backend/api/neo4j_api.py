from flask import Blueprint, request, jsonify
from neo4j import GraphDatabase

neo4j_api = Blueprint('neo4j_api', __name__)

class Neo4jConnection:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def query(self, query, parameters=None):
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

@neo4j_api.route('/query', methods=['POST'])
def execute_query():
    data = request.json
    query = data.get('query')
    parameters = data.get('parameters', {})
    
    if not query:
        return jsonify({'error': 'Query is required'}), 400

    try:
        neo4j_conn = Neo4jConnection(uri='bolt://localhost:7687', user='neo4j', password='your_password')
        result = neo4j_conn.query(query, parameters)
        neo4j_conn.close()
        return jsonify(result)
    except Exception as e:
        return jsonify({'error': str(e)}), 500