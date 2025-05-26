from flask import Flask, jsonify
from flask_cors import CORS  # 新增
from neo4j import GraphDatabase

app = Flask(__name__)
CORS(app)  # 新增，允许所有来源跨域

# Neo4j 配置
uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))

@app.route('/api/graph')
def get_graph():
    nodes = []
    links = []
    node_ids = set()
    with driver.session() as session:
        # 查询所有部门和事项及其关系
        result = session.run("""
            MATCH (d:Department)-[:管理]->(m:Matter)
            RETURN d.name AS dept, m.code AS code, m.name AS matter
        """)
        for record in result:
            # 添加部门节点
            if record["dept"] not in node_ids:
                nodes.append({"id": record["dept"], "group": "department"})
                node_ids.add(record["dept"])
            # 添加事项节点
            if record["matter"] not in node_ids:
                nodes.append({"id": record["matter"], "group": "matter"})
                node_ids.add(record["matter"])
            # 添加关系
            links.append({"source": record["dept"], "target": record["matter"]})
    return jsonify({"nodes": nodes, "links": links})

if __name__ == '__main__':
    app.run(port=5000)