from pymongo import MongoClient
import os
import glob
import json 

class MongoDatabase:
    client = MongoClient(os.environ['MONGO_CONNECTION_STRING'])
    
    def load_geometries():
        json_files = glob.glob(os.path.join(os.getcwd(), 'archive', '*.json'))
        for file_path in json_files:
            file = open(file_path)
            data = json.load(file)
