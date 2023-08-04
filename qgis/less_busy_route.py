from qgis.core import QgsProject, QgsFeatureRequest
from neo4j import GraphDatabase

location = "anderlecht"
source = 9
target = 2751
start_date = '2019-01-14 00:00:00'
end_date = '2019-01-25 00:00:00'
number_of_paths = 5

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
session = driver.session()

with driver.session() as session:
    min_trucks = None
    path = []
    avoid = []
    layer = QgsProject.instance().mapLayersByName(location)[0]
    for j in range(number_of_paths):
        query = """
        MATCH (s1:StreetSection {location: $location, street_id: $source}),
        (s2:StreetSection {location: $location, street_id: $target}),
        p = shortestPath((s1)-[:IS_CONNECTED*]-(s2))
        WHERE all(node IN nodes(p) WHERE node.location = $location AND NOT node.street_id in $avoid)
        UNWIND nodes(p) as node
        MATCH (m:Measure)-[:MEASURED]->(node) WHERE m.avg_speed < 200 AND m.interval = 5 AND datetime(replace(m.timestamp , ' ', 'T')) > datetime(replace($start_date, ' ', 'T'))
        AND datetime(replace(m.timestamp , ' ', 'T')) < datetime(replace($end_date, ' ', 'T'))
        RETURN nodes(p) as path, SUM(m.trucks_count) as trucks
        """
        results = session.run(query, {"avoid": avoid, "location": location, "source": source, "target": target, "start_date": start_date, "end_date": end_date})
        
        for record in results:
            current_path = []
            for i, node in enumerate(record['path']):
                if(i > 0 and i < len(record['path']) - 1 and node._properties['street_id'] not in avoid):
                    avoid.append(node._properties['street_id'])
                current_path.append(node._properties['street_id'])
            
            trucks = record.data()['trucks']
            if(j == 0):
                min_trucks = trucks
                path = current_path[:]
            else:
                if(trucks < min_trucks):
                    min_trucks = trucks
                    path = current_path[:]
    ids = []
    
    for street_id in path:
        request = QgsFeatureRequest().setFilterExpression(f'street_id = \'{street_id}\'')
        features = layer.getFeatures(request)
        for feature in features:
            ids.append(feature['id'])
                
    new_layer = layer.materialize(QgsFeatureRequest().setFilterFids(ids))
    new_layer.setName('less_busy_route')
    QgsProject.instance().addMapLayer(new_layer)
   
driver.close()
