CREATE CONSTRAINT FOR (g:Government) REQUIRE g.id IS UNIQUE;

CREATE (:Government {id: '1', name: 'Ministry of Finance', description: 'Responsible for financial and economic policy.'});
CREATE (:Government {id: '2', name: 'Ministry of Health', description: 'Oversees public health and healthcare services.'});
CREATE (:Government {id: '3', name: 'Ministry of Education', description: 'Responsible for education policy and institutions.'});

MATCH (a:Government {id: '1'}), (b:Government {id: '2'})
CREATE (a)-[:COLLABORATES_WITH]->(b);

MATCH (a:Government {id: '1'}), (b:Government {id: '3'})
CREATE (a)-[:COLLABORATES_WITH]->(b);

MATCH (a:Government {id: '2'}), (b:Government {id: '3'})
CREATE (a)-[:COLLABORATES_WITH]->(b);

MATCH (g:Government)
RETURN g;

MATCH (g:Government {id: '1'})
SET g.description = 'Updated description for Ministry of Finance';

MATCH (g:Government {id: '2'})
DELETE g;