from qgis.core import QgsProject, QgsFeatureRequest
from neo4j import GraphDatabase

location = "anderlecht"
sub_graph = "anderlecht-subgraph"
depth = 1000
source = 9 

driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j","{your_neo4j_password}"))
session = driver.session()

with driver.session() as session:
    query = """
    MATCH (source: StreetSection{location: $location, street_id: $source})
    CALL gds.dfs.stream($sub_graph, {
      sourceNode: source,
      maxDepth: $depth
    })
    YIELD path
    RETURN nodes(path) as path
    """
    
    results = session.run(query, {"source": source, "depth": depth, "location": location, "sub_graph": sub_graph})
    layer = QgsProject.instance().mapLayersByName(location)[0]
    
    for record in results:
        for node in record['path']:
            street_id = node._properties['street_id']
            request = QgsFeatureRequest().setFilterExpression(f'street_id = \'{street_id}\'')
            features = layer.getFeatures(request)
            for feature in features:
                ids.append(feature['id'])

    new_layer = layer.materialize(QgsFeatureRequest().setFilterFids(ids))
    new_layer.setName('dfs  ')
    QgsProject.instance().addMapLayer(new_layer)

driver.close()

