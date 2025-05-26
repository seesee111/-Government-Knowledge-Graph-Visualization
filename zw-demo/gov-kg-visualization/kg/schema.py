class Schema:
    def __init__(self):
        self.nodes = {
            "GovernmentAgency": {
                "properties": {
                    "name": "string",
                    "type": "string",
                    "location": "string"
                }
            },
            "Policy": {
                "properties": {
                    "title": "string",
                    "description": "string",
                    "date": "date"
                }
            },
            "Citizen": {
                "properties": {
                    "name": "string",
                    "age": "int",
                    "location": "string"
                }
            }
        }
        
        self.relationships = {
            "HAS_POLICY": {
                "from": "GovernmentAgency",
                "to": "Policy",
                "properties": {}
            },
            "INTERESTED_IN": {
                "from": "Citizen",
                "to": "Policy",
                "properties": {}
            }
        }

    def validate_node(self, node_type, properties):
        if node_type not in self.nodes:
            raise ValueError(f"Invalid node type: {node_type}")
        
        schema = self.nodes[node_type]["properties"]
        for key, value in properties.items():
            if key not in schema:
                raise ValueError(f"Invalid property: {key} for node type: {node_type}")
            if not isinstance(value, eval(schema[key])):
                raise ValueError(f"Invalid type for property: {key}. Expected {schema[key]}, got {type(value).__name__}")

    def validate_relationship(self, relationship_type, from_node, to_node):
        if relationship_type not in self.relationships:
            raise ValueError(f"Invalid relationship type: {relationship_type}")
        
        rel = self.relationships[relationship_type]
        if from_node != rel["from"] or to_node != rel["to"]:
            raise ValueError(f"Invalid relationship: {from_node} -> {to_node} for relationship type: {relationship_type}")