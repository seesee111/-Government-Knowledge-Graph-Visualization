from flask import Blueprint, request, jsonify
from neo4j import GraphDatabase

# 创建一个 Flask 蓝图，用于注册 Neo4j 相关的路由
neo4j_api = Blueprint('neo4j_api', __name__)

# Neo4j 数据库连接类
class Neo4jConnection:
    def __init__(self, uri, user, password):
        # 初始化数据库驱动
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # 关闭数据库连接
        self.driver.close()

    def query(self, query, parameters=None):
        # 执行 Cypher 查询，并返回结果
        with self.driver.session() as session:
            result = session.run(query, parameters)
            return [record.data() for record in result]

# 定义一个 POST 路由，用于执行前端传来的 Cypher 查询
@neo4j_api.route('/query', methods=['POST'])
def execute_query():
    data = request.json
    query = data.get('query')
    parameters = data.get('parameters', {})
    
    if not query:
        # 如果没有提供查询语句，返回错误信息
        return jsonify({'error': 'Query is required'}), 400

    try:
        # 创建 Neo4j 连接，执行查询
        neo4j_conn = Neo4jConnection(uri='bolt://localhost:7687', user='neo4j', password='12345678')
        result = neo4j_conn.query(query, parameters)
        neo4j_conn.close()
        return jsonify(result)
    except Exception as e:
        # 查询出错时返回错误信息
        return jsonify({'error': str(e)}), 500

# Neo4jAPI 类，封装节点和关系的获取方法
class Neo4jAPI:
    def __init__(self):
        # 这里请根据实际情况填写数据库连接信息
        self.conn = Neo4jConnection(uri='bolt://localhost:7687', user='neo4j', password='12345678')

    def get_all_nodes(self):
        # 获取所有节点
        query = "MATCH (n) RETURN n"
        result = self.conn.query(query)
        return [record['n'] for record in result]

    def get_all_relationships(self):
        # 获取所有关系
        query = "MATCH ()-[r]->() RETURN r"
        result = self.conn.query(query)
        return [record['r'] for record in result]

# 新增：获取所有节点的路由
@neo4j_api.route('/nodes', methods=['GET'])
def api_get_nodes():
    api = Neo4jAPI()
    nodes = api.get_all_nodes()
    return jsonify(nodes)

# 新增：获取所有关系的路由
@neo4j_api.route('/relationships', methods=['GET'])
def api_get_relationships():
    api = Neo4jAPI()
    relationships = api.get_all_relationships()
    return jsonify(relationships)