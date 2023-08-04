import json
streets = open('streets.txt', 'w')
file = open('archive\\Anderlecht_streets.json')
lines = file.read()
tmp = json.loads(lines)
for i, poly in enumerate(tmp['features']):
    tmp = str(poly['geometry']).replace("'", '"')
    streets.write("""
    INSERT INTO streets (street_id, location, geometry)
VALUES ('""" +str(i) +"""', 'anderlecht','"""+tmp+"""');
    """)
file.close()
file = open('archive\\Belgium_streets.json')
lines = file.read()
tmp = json.loads(lines)
for i, poly in enumerate(tmp['features']):
    tmp = str(poly['geometry']).replace("'", '"')
    streets.write("""
    INSERT INTO streets (street_id, location, geometry)
VALUES ('""" +str(i) +"""', 'belgium','"""+tmp+"""');
    """)
file.close()
file = open('archive\\Bruxelles_streets.json')
lines = file.read()
tmp = json.loads(lines)
for i, poly in enumerate(tmp['features']):
    tmp = str(poly['geometry']).replace("'", '"')
    streets.write("""
    INSERT INTO streets (street_id, location, geometry)
VALUES ('""" +str(i) +"""', 'bruxelles','"""+tmp+"""');
    """)
file.close()
streets.close()

