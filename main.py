from flask import Flask, render_template, request
from databases.mongodb import MongoDatabase
from databases.neo4j import Neo4jDatabase
import json 

app = Flask(__name__)

@app.route("/")
def root():
    return render_template('index.html')

@app.route("/osm")
def osm():
    return render_template('osm.html')

@app.route("/measurements")
def measurements():
    return render_template('measurements.html')

@app.post('/geometries')
def geometries():
    MongoDatabase.load_geometries()
    return {
        "status": 200,
        "message": "Geometrie ricaricate con successo"
    }

@app.delete('/geometries')
def delete_geometries():
    MongoDatabase.delete_geometries()
    return {
        "status": 200,
        "message": "Geometrie eliminate con successo"
    }

@app.get('/streets')
def retrieve_streets():
    streets = MongoDatabase.retrieve_streets(location=request.args.get('location'))
    return {
        "status": 200,
        "message": "Geometrie ricaricate con successo",
        "streets": streets,
    }

@app.get('/boundaries')
def retrieve_boundaries():
    streets = MongoDatabase.retrieve_boundaries(location=request.args.get('location'))
    return {
        "status": 200,
        "message": "Geometrie ricaricate con successo",
        "streets": streets,
    }

@app.get('/locations')
def retrieve_locations():
    locations = MongoDatabase.retrieve_locations()
    return {
        "status": 200,
        "message": "Geometrie ricaricate con successo",
        "locations": locations,
    }

@app.get('/test')
def test():
    #Neo4jDatabase.load_streets()
    Neo4jDatabase.load_trucks()
    return {
        "status": 200,
        
    }




