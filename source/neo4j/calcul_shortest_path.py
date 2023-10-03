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