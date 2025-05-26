import json
from neo4j import GraphDatabase

class KnowledgeGraphBuilder:
    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_node(self, label, properties):
        with self.driver.session() as session:
            session.write_transaction(self._create_node, label, properties)

    @staticmethod
    def _create_node(tx, label, properties):
        query = f"CREATE (n:{label} $properties)"
        tx.run(query, properties=properties)

    def create_relationship(self, start_label, start_id, end_label, end_id, relationship_type):
        with self.driver.session() as session:
            session.write_transaction(self._create_relationship, start_label, start_id, end_label, end_id, relationship_type)

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
            # Assuming item contains 'label' and 'properties' for nodes
            self.create_node(item['label'], item['properties'])
            # Assuming relationships are defined in item['relationships']
            for rel in item.get('relationships', []):
                self.create_relationship(rel['start_label'], rel['start_id'], rel['end_label'], rel['end_id'], rel['type'])

if __name__ == "__main__":
    # Example usage
    uri = "bolt://localhost:7687"
    user = "neo4j"
    password = "your_password"

    kg_builder = KnowledgeGraphBuilder(uri, user, password)

    # Sample data to build the knowledge graph
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