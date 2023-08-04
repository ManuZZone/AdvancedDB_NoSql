from neo4j import GraphDatabase
import os
import glob
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
with driver.session() as session:
    locations = ['anderlecht', 'belgium', 'bruxelles']
    for location in locations:
        paths = glob.glob(os.path.join(os.getcwd(), 'archive', 'groups', location, '*.csv'))
        for path in paths:
            street_id = path.split("\\")[-1].split(".")[0]
            template_load_csv = 'LOAD CSV FROM "file:///groups/{}/{}.csv" AS row\n'.format(location, street_id)
            template_load_csv += """
            MATCH (s:StreetSection {street_id: toInteger($street_id), location: toString($location)})
            CALL{
                WITH row
                CREATE (m:Measure {timestamp: toString(row[0]), trucks_count: toInteger(row[2]), avg_speed: toFloat(row[3]), interval: toInteger(row[4])})
                CREATE (m)-[:MEASURED]->(s)
            } IN TRANSACTIONS OF 10000 ROWS
            """
            session.run(template_load_csv, {"street_id": street_id, "location":location})

