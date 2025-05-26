from neo4j import GraphDatabase

uri = "bolt://localhost:7687"
user = "neo4j"
password = "12345678"

driver = GraphDatabase.driver(uri, auth=(user, password))

with driver.session() as session:
    # 清除所有节点和关系
    session.run("MATCH (n) DETACH DELETE n")
    # 删除所有约束
    constraints = session.run("SHOW CONSTRAINTS")
    for record in constraints:
        name = record["name"]
        session.run(f"DROP CONSTRAINT {name} IF EXISTS")
    # 删除所有索引
    indexes = session.run("SHOW INDEXES")
    for record in indexes:
        name = record["name"]
        session.run(f"DROP INDEX {name} IF EXISTS")

driver.close()