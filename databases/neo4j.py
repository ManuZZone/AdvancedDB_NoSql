from neo4j import GraphDatabase
import os
from databases.mongodb import MongoDatabase
import glob
import csv
import platform

osname = platform.platform()

class Neo4jDatabase:
    client = GraphDatabase.driver(os.environ['NEO4J_CONNECTION_STRING'], auth=(os.environ['NEO4J_USERNAME'],os.environ['NEO4J_PASSWORD']))

    def _create_street(session, street_id: int):
        query = """
        CREATE (s:Street {streetId: $streetId})
        """
        parameters = {"streetId": street_id}
        session.run(query, parameters)

    def _create_truck(session):
        query = """
        CREATE (s:Truck) RETURN id(s) as truck_id
        """
        parameters = {}
        return session.run(query, parameters)

    def _create_travelled_relationship(session, truck_id, street_id, timestamp, avg_speed, interval):
        query = """
        MATCH (n1:Truck), (n2:Street)
        WHERE ID(n1) = $truck_id AND ID(n2) = $street_id
        CREATE (n1)-[r:TRAVELLED_IN]->(n2)
        SET r.timestamp = $timestamp, r.avg_speed = $avg_speed, r.interval = $interval
        RETURN r
        """
       
        parameters = {"truck_id": truck_id, "street_id": street_id, "timestamp": timestamp, "avg_speed": avg_speed, "interval": interval}
        session.run(query, parameters)

    def load_streets():
        streets = []
        locations = MongoDatabase.retrieve_locations()
        for location in locations:
            streets += MongoDatabase.retrieve_streets(location=location)
        with Neo4jDatabase.client.session() as session:
            session.run("MATCH (n:Street) DELETE n""")
            for street in streets:
                Neo4jDatabase._create_street(session=session, street_id=int(street['street_id']))

    def load_trucks():
        json_files = glob.glob(os.path.join(os.getcwd(), 'archive', '*.csv'))
        with Neo4jDatabase.client.session() as session:
            session.run("MATCH (n:Truck) DELETE n""")
            for file_path in json_files:
                if(osname.startswith('Windows')):
                    location = file_path.split("\\")
                else:
                    location = file_path.split("/")
                interval = int(location[-1].split("_")[1].replace("min", ""))
                with open(file_path, 'r') as csv_file:
                    reader = csv.reader(csv_file)
                    for row in reader:
                        timestamp = row[0]
                        street_id = row[1]
                        trucks_number = row[2]
                        avg_speed = row[3]
                        for i in range(0, int(trucks_number)):
                            result = Neo4jDatabase._create_truck(session)
                            truck_id = result.single()['truck_id']
                            Neo4jDatabase._create_travelled_relationship(session, int(truck_id), int(float(street_id)), timestamp, avg_speed, interval)
                        
            
