from qgis.core import QgsProject, QgsFeatureRequest
from neo4j import GraphDatabase

location = "anderlecht"
target_location = "bruxelles"
source = 1917
target = 1500
ids = {}
ids[location] = []
ids[target_location] = []
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
session = driver.session()

with driver.session() as session:
    query = """
    MATCH (s1:StreetSection {location: $location, street_id: $source}),
    (s2:StreetSection {location: $target_location, street_id: $target}),
    p = shortestPath((s1)-[:IS_CONNECTED*]-(s2)) 
    WHERE all(node IN nodes(p) WHERE node.location <> "belgium" )
    RETURN nodes(p) as path
    """
    
    results = session.run(query,    {"source": source, "target": target, "location": location, "target_location": target_location})
    
    for record in results:
        for node in record['path']:
            street_id = node._properties['street_id']
            request = QgsFeatureRequest().setFilterExpression(f'street_id = \'{street_id}\'')
            layer = QgsProject.instance().mapLayersByName(node._properties['location'])[0]
            
            features = layer.getFeatures(request)
            for feature in features:
                ids[node._properties['location']].append(feature['id'])
                 
    for location in ids:
        layer = QgsProject.instance().mapLayersByName(location)[0]
        new_layer = layer.materialize(QgsFeatureRequest().setFilterFids(ids[location]))
        new_layer.setName('all_shortest_paths_' + str(location   ))
        QgsProject.instance().addMapLayer(new_layer)

driver.close()

