from flask import Flask, jsonify
from flask_cors import CORS
from neo4j import GraphDatabase
import re

app = Flask(__name__)
CORS(app)

# Neo4j数据库连接配置（请根据实际情况修改）
uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"
driver = GraphDatabase.driver(uri, auth=(user, password))

# 编码映射表
DEPT_MAP = {
    "9": "公安", "11": "民政", "15": "国土", "16": "环保", "17": "住建", "18": "交通运输", "20": "农委",
    "21": "商务", "22": "文化与旅游", "23": "卫计", "24": "退役军人", "25": "安监", "30": "地税",
    "31": "市场", "39": "新闻出版广电", "64": "林业", "72": "药监", "73": "知识产权", "75": "档案",
    "76": "保密", "99": "其他"
}
MATTER_TYPE_MAP = {
    "99": "空白", "10": "其他行政权力", "9": "行政裁决", "2": "行政处罚", "5": "行政给付",
    "6": "行政检查", "3": "行政强制", "1": "行政许可", "4": "行政征收", "20": "行政征收"
}
LEVEL_MAP = {
    "2": "市", "3": "县", "4": "镇（乡、街道)级", "1": "省"
}

def map_multi_values(val, mapping):
    """支持多值（如'2,3,4'）的映射"""
    if not val:
        return ""
    return ",".join([mapping.get(v.strip().lstrip("0"), v.strip()) for v in str(val).split(",")])

def try_map(val):
    for mapping in (LEVEL_MAP, MATTER_TYPE_MAP, DEPT_MAP):
        mapped = map_multi_values(val, mapping)
        if mapped != val:
            return mapped
    return val

@app.route('/api/graph')
def get_graph():
    nodes = []
    links = []
    node_ids = set()
    with driver.session() as session:
        result = session.run("""
            MATCH (n)
            OPTIONAL MATCH (n)-[r]->(m)
            RETURN n, type(r) AS rel_type, m
        """)
        for record in result:
            n = record["n"]
            m = record["m"]
            rel_type = record["rel_type"]

            # 只保留原始属性，不做任何映射
            n_id = n.get("code") or n.get("name") or n.get("value")
            n_group = list(n.labels)[0].lower() if n.labels else "other"
            if n_id and n_id not in node_ids:
                node_data = dict(n)
                node_data["id"] = n_id
                node_data["group"] = n_group
                node_data["name"] = n.get("name") or n.get("value")
                nodes.append(node_data)
                node_ids.add(n_id)

            if m:
                m_id = m.get("code") or m.get("name") or m.get("value")
                m_group = list(m.labels)[0].lower() if m.labels else "other"
                if m_id and m_id not in node_ids:
                    node_data = dict(m)
                    node_data["id"] = m_id
                    node_data["group"] = m_group
                    node_data["name"] = m.get("name") or m.get("value")
                    nodes.append(node_data)
                    node_ids.add(m_id)
                if rel_type:
                    links.append({
                        "source": n_id,
                        "target": m_id,
                        "type": rel_type
                    })
    return jsonify({"nodes": nodes, "links": links})

if __name__ == '__main__':
    app.run(port=5000)