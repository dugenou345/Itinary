MATCH (a:Address)-[:NEAREST_INTERSECTION]->(source:Intersection)
WHERE a.full_address CONTAINS "410 E 5TH AVE SAN MATEO, CA"
MATCH 
  (poi:Address)-[:NEAREST_INTERSECTION]->(dest:Intersection) 
WHERE poi.full_address CONTAINS "111 5TH AVE"
CALL apoc.algo.dijkstra(source, dest, "ROAD_SEGMENT", "length") 
YIELD weight, path
RETURN *
//WITH [ x in nodes(path) | {latitude: x.location.latitude, longitude: x.location.longitude}] AS route, weight AS totalDist
//RETURN *

MATCH (poi_source:PointOfInterest)-[:NEAREST_INTERSECTION]->(source:Intersection)
WHERE poi_source.name CONTAINS "Notre Dame"
MATCH 
  (poi_dest:PointOfInterest)-[:NEAREST_INTERSECTION]->(dest:Intersection) 
WHERE poi_dest.name CONTAINS "Tour Eiffel"
CALL apoc.algo.dijkstra(source, dest, "ROAD_SEGMENT", "length") 
YIELD weight, path
RETURN *
//WITH [ x in nodes(path) | {latitude: x.location.latitude, longitude: x.location.longitude}] AS route, weight AS totalDist
//RETURN *


CALL db.index.fulltext.queryNodes("search_index", $searchString) 
YIELD node, score
RETURN coalesce(node.name, node.full_address) AS value, score, labels(node)[0] AS label, node.id AS id
ORDER BY score DESC LIMIT 25
MATCH (to {id: $dest})-[:NEAREST_INTERSECTION]->(source:Intersection) 
MATCH (from {id: $source})-[:NEAREST_INTERSECTION]->(target:Intersection)
CALL apoc.algo.dijkstra(source, target, 'ROAD_SEGMENT', 'length')
YIELD path, weight
RETURN [n in nodes(path) | [n.location.latitude, n.location.longitude]] AS route