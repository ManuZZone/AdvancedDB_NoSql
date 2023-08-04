from neo4j import GraphDatabase
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
session = driver.session()
with driver.session() as session:
    template_load_csv = """
    LOAD CSV FROM "file:///streets_section/streets.csv" AS row
    CALL{
        WITH row
        CREATE (s:StreetSection {pg_id: toInteger(row[0]), street_id: toInteger(row[1]), location: toString(row[2])})
    } IN TRANSACTIONS OF 10000 ROWS
    """
    session.run(template_load_csv)
