from flask import Flask, jsonify
from flask_cors import CORS
from api.neo4j_api import Neo4jAPI

app = Flask(__name__)
CORS(app)

neo4j_api = Neo4jAPI()

@app.route('/api/nodes', methods=['GET'])
def get_nodes():
    nodes = neo4j_api.get_all_nodes()
    return jsonify(nodes)

@app.route('/api/relationships', methods=['GET'])
def get_relationships():
    relationships = neo4j_api.get_all_relationships()
    return jsonify(relationships)

if __name__ == '__main__':
    app.run(debug=True)