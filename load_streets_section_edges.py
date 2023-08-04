from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
with driver.session() as session:
    template_load_csv = """
    LOAD CSV FROM "file:///streets_section/edge.csv" AS row
    CALL{
        WITH row
        MATCH (n1:StreetSection {pg_id: toInteger(row[0])}), (n2:StreetSection {pg_id: toInteger(row[1])})
        MERGE (n1)-[:IS_CONNECTED]-(n2)
    } IN TRANSACTIONS OF 10000 ROWS
    """
    session.run(template_load_csv)
