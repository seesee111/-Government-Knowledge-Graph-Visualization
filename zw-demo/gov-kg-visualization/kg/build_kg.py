import json
from neo4j import GraphDatabase

class KnowledgeGraphBuilder:
    def __init__(self, uri, user, password):
        # 初始化Neo4j数据库连接
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        # 关闭数据库连接
        self.driver.close()

    def create_department(self, name):
        # 创建或获取“部门”节点
        with self.driver.session() as session:
            session.run("MERGE (d:Department {name: $name})", name=name)

    def create_matter(self, code, name, qlkind, lawbasis, level):
        # 创建或获取“事项”节点，并设置属性
        with self.driver.session() as session:
            session.run(
                "MERGE (m:Matter {code: $code}) "
                "SET m.name=$name, m.type=$qlkind, m.basis=$lawbasis, m.level=$level",
                code=code, name=name, qlkind=qlkind, lawbasis=lawbasis, level=level
            )

    def create_relationship(self, dept_name, matter_code):
        # 创建“部门”与“事项”之间的“管理”关系
        with self.driver.session() as session:
            session.run(
                "MATCH (d:Department {name: $dept_name}), (m:Matter {code: $matter_code}) "
                "MERGE (d)-[:管理]->(m)",
                dept_name=dept_name, matter_code=matter_code
            )

    def build_knowledge_graph(self, data):
        # 根据数据批量构建知识图谱
        for item in data:
            dept = item.get("授权部门", "")
            code = item.get("职权编码", "")
            name = item.get("事项名称", "")
            qlkind = item.get("事项类型", "")
            lawbasis = item.get("依据", "")
            level = item.get("实施层级", "")
            if dept and code:
                self.create_department(dept)
                self.create_matter(code, name, qlkind, lawbasis, level)
                self.create_relationship(dept, code)

if __name__ == "__main__":
    # 配置Neo4j数据库连接信息
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "12345678"

    kg_builder = KnowledgeGraphBuilder(uri, user, password)

    # 读取 government_data.json 文件
    with open("government_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 构建知识图谱
    kg_builder.build_knowledge_graph(data)
    kg_builder.close()