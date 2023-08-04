from qgis.core import QgsProject, QgsFeatureRequest
from neo4j import GraphDatabase
import processing
import random
processing.algorithmHelp("native:mergevectorlayers")

location = "anderlecht"
source = 9
target = 2751
start_date = '2019-01-14 00:00:00'
end_date = '2019-01-25 00:00:00'
number_of_paths = 5
measure_interval = 5

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
session = driver.session()

with driver.session() as session:    
    ids = []
    avoid = []
    layers = []
    layer = QgsProject.instance().mapLayersByName(location)[0]
    for j in range(number_of_paths):
        ids = []
        query = """
        MATCH (s1:StreetSection {location: $location, street_id: $source}),
        (s2:StreetSection {location: $location, street_id: $target}),
        p = shortestPath((s1)-[:IS_CONNECTED*]-(s2))
        WHERE all(node IN nodes(p) WHERE node.location = $location AND NOT node.street_id in $avoid)
        UNWIND nodes(p) as node
        MATCH (m:Measure)-[:MEASURED]->(node) WHERE m.avg_speed < 200 AND m.interval = $interval AND datetime(replace(m.timestamp , ' ', 'T')) > datetime(replace($start_date, ' ', 'T'))
        AND datetime(replace(m.timestamp , ' ', 'T')) < datetime(replace($end_date, ' ', 'T'))
        RETURN nodes(p) as path, AVG(m.avg_speed) as media
        """
        results = session.run(query, {"avoid": avoid, "location": location, "source": source, "target": target, "start_date": start_date, "end_date": end_date, "interval": measure_interval})
        
        for record in results:
            path = []
            for i, node in enumerate(record['path']):
                if(i > 0 and i < len(record['path']) - 1 and node._properties['street_id'] not in avoid):
                    avoid.append(node._properties['street_id'])
                path.append(node._properties['street_id'])
                
        
        for street_id in path:
            request = QgsFeatureRequest().setFilterExpression(f'street_id = \'{street_id}\'')
            features = layer.getFeatures(request)
            for feature in features:
                ids.append(feature['id'])
        layers.append(layer.materialize(QgsFeatureRequest().setFilterFids(ids)))
    """
    color = ["#"+''.join([random.choice('0123456789ABCDEF') for j in range(6)]) for i in range(number_of_paths)]
    print(color)
    for i, layer in enumerate(layers):
        print(color[i])
        layer.renderer().symbol().setColor(QColor(color[i]))
    """
    processing.runAndLoadResults("native:mergevectorlayers", {'LAYERS': layers, 'OUTPUT': "memory:n_different_shortest_paths"})
    QgsProject.instance().addMapLayer(new_layer)
    
driver.close()

