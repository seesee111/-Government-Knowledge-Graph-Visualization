import json
from neo4j import GraphDatabase

class KnowledgeGraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            session.execute_write(self._create_node, label, properties)

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} $properties)"
        tx.run(query, properties=properties)

    def create_relationship(self, start_label, start_id, end_label, end_id, relationship_type):
        with self.driver.session() as session:
            session.execute_write(self._create_relationship, start_label, start_id, end_label, end_id, relationship_type)

    @staticmethod
    def _create_relationship(tx, start_label, start_id, end_label, end_id, relationship_type):
        query = f"""
        MATCH (a:{start_label}), (b:{end_label})
        WHERE a.id = $start_id AND b.id = $end_id
        CREATE (a)-[r:{relationship_type}]->(b)
        """
        tx.run(query, start_id=start_id, end_id=end_id)

    def build_knowledge_graph(self, data):
        for item in data:
            # 假设 item 包含节点的 'label' 和 'properties'
            self.create_node(item['label'], item['properties'])
            # 假设关系定义在 item['relationships'] 中
            for rel in item.get('relationships', []):
                self.create_relationship(rel['start_label'], rel['start_id'], rel['end_label'], rel['end_id'], rel['type'])

if __name__ == "__main__":
    # 示例用法
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "12345678"

    kg_builder = KnowledgeGraphBuilder(uri, user, password)

    # 用于构建知识图谱的示例数据
    sample_data = [
        {
            "label": "GovernmentAgency",
            "properties": {"id": 1, "name": "Agency A"},
            "relationships": [
                {"start_label": "GovernmentAgency", "start_id": 1, "end_label": "GovernmentAgency", "end_id": 2, "type": "COLLABORATES_WITH"}
            ]
        },
        {
            "label": "GovernmentAgency",
            "properties": {"id": 2, "name": "Agency B"},
            "relationships": []
        }
    ]

    kg_builder.build_knowledge_graph(sample_data)
    kg_builder.close()