from neo4j import GraphDatabase
import os

class Neo4jDatabase:
    client = GraphDatabase.driver(os.environ['NEO4J_CONNECTION_STRING'], auth=(os.environ['NEO4J_USERNAME'],os.environ['NEO4J_PASSWORD']))