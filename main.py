from flask import Flask, render_template
from databases.mongodb import MongoDatabase
from databases.neo4j import Neo4jDatabase

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.post('/geometries')
def geometries():
    MongoDatabase.load_geometries()
    return {
        "status": 200,
        "message": "Geometrie ricaricate con successo"
    }

print(MongoDatabase.client)
print(Neo4jDatabase.client)

