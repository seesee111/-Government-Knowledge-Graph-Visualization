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
        with self.driver.session() as session:
            session.run("MERGE (d:Department {name: $name, value: $name})", name=name)

    def create_matter(self, code, name):
        with self.driver.session() as session:
            session.run(
                "MERGE (m:Matter {code: $code}) SET m.name=$name, m.value=$name",
                code=code, name=name
            )

    def create_content(self, content_type, value):
        # 创建或获取“内容”节点，name与value一致
        with self.driver.session() as session:
            session.run(
                "MERGE (c:Content {type: $type, value: $value}) "
                "SET c.name = $value",
                type=content_type, value=value
            )

    def create_relationships(self, dept, code, qlkind, lawbasis, level):
        # 创建节点之间的关系
        with self.driver.session() as session:
            # 部门-事项
            session.run(
                "MATCH (d:Department {name: $dept}), (m:Matter {code: $code}) "
                "MERGE (d)-[:管理]->(m)",
                dept=dept, code=code
            )
            # 事项-事项类型
            if qlkind:
                session.run(
                    "MATCH (m:Matter {code: $code}), (c:Content {type: '事项类型', value: $value}) "
                    "MERGE (m)-[:包括]->(c)",
                    code=code, value=qlkind
                )
            # 事项-实施层级
            if level:
                session.run(
                    "MATCH (m:Matter {code: $code}), (c:Content {type: '实施层级', value: $value}) "
                    "MERGE (m)-[:包括]->(c)",
                    code=code, value=level
                )
            # 事项-依据（整体作为一个节点）
            if lawbasis:
                session.run(
                    "MATCH (m:Matter {code: $code}), (c:Content {type: '依据', value: $value}) "
                    "MERGE (m)-[:包括]->(c)",
                    code=code, value=lawbasis
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
                self.create_matter(code, name)
                if qlkind:
                    self.create_content("事项类型", qlkind)
                if level:
                    self.create_content("实施层级", level)
                if lawbasis:
                    self.create_content("依据", lawbasis)
                self.create_relationships(
                    dept, code, qlkind, lawbasis, level
                )

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