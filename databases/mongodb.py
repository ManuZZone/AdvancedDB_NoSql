from pymongo import MongoClient
import os
import glob
import json 
import platform
from shapely.geometry import Polygon
osname = platform.platform()

class MongoDatabase:
    client = MongoClient(os.environ['MONGO_CONNECTION_STRING'])
    
    def retrieve_streets(location):
        ret = []
        streets = MongoDatabase.client['freight_transport_geometries']['streets'].find({"location": location })
        for street in streets:
            ret.append({
                "street_id": street['street_id'],
                "location": street['location'],
                "type": street['type'],
                "properties": street['properties'],
                "geometry": street['geometry']
            })
        return ret
    
    def retrieve_boundaries(location):
        return

    def _check_adjacency(polygon_1_coordinates, polygon_2_coordinates):
        polygon_1 = Polygon(polygon_1_coordinates)
        polygon_2 = Polygon(polygon_2_coordinates)
        return polygon_1.touches(polygon_2)

    def load_geometries():
        MongoDatabase.client['freight_transport_geometries']['streets'].delete_many({})
        json_files = glob.glob(os.path.join(os.getcwd(), 'archive', '*.json'))
        for file_path in json_files:
            file = open(file_path)
            data = json.load(file)
            if(osname.startswith('Windows')):
                location = file_path.split("\\")
            else:
                location = file_path.split("/")
            if("streets" in location[-1].lower()):
                location = location[-1].lower().split("_")[0]
                streets = data['features']
                for i in range(0, len(streets)):
                    curr = {
                        "street_id": i,
                        "location": location,
                        "adjacencies_streets": []
                    }
                    curr.update(streets[i])
                    streets[i] = curr

                for i in range(0, len(streets)):
                    for j in range(0, len(streets)):
                        if(MongoDatabase._check_adjacency(streets[i]['geometry']['coordinates'][0], streets[j]['geometry']['coordinates'][0])):
                            if(streets[j]['street_id'] not in streets[i]['adjacencies_streets']):
                                streets[i]['adjacencies_streets'].append(streets[j]['street_id'])
                            if(streets[i]['street_id'] not in streets[j]['adjacencies_streets']):
                                streets[j]['adjacencies_streets'].append(streets[i]['street_id'])
                    MongoDatabase.client['freight_transport_geometries']['streets'].insert_one(streets[i])
                """
                for i in range(len(data['features'])):
                    curr = {
                        "street_id": i,
                        "location": location,
                    }
                    curr.update(data['features'][i])
                    data['features'][i] = curr
                    for j in range(len(data['features'])):
                        if i == j:
                            continue
                        if(MongoDatabase._check_adjacency( data['features'][i],  data['features'][j])):
                            data['features'][i]
                """   
                    
                #MongoDatabase.client['freight_transport_geometries']['streets'].insert_many(streets)
            else:
                location = location[-1].lower().split(".")[0]
                for i in range(len(data['geometries'])):
                    curr = {
                        "geometry_id": i,
                        "location": location,
                    }
                    curr.update(data['geometries'][i])
                    data['geometries'][i] = curr
                MongoDatabase.client['freight_transport_geometries']['boundaries'].insert_many(data['geometries'])
          
    def retrieve_locations():
        return MongoDatabase.client['freight_transport_geometries']['streets'].distinct("location")
        
    
    def delete_geometries():
        MongoDatabase.client['freight_transport_geometries']['streets'].delete_many({})
        
