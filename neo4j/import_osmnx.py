import osmnx as ox
import matplotlib as mp
import os

os.environ['MPLBACKEND'] = 'Qt5Agg'  # Replace 'TkAgg' with your preferred backend


print(ox.__version__)
print(mp.__version__)

G = ox.graph_from_place("Melun, France", network_type= "drive")

#fig, ax = ox.plot_graph(G)


gdf_nodes, gdf_relationships = ox.graph_to_gdfs(G)
gdf_nodes.reset_index(inplace=True)
gdf_relationships.reset_index(inplace=True)

gdf_nodes.plot(markersize=0.1)
print(gdf_nodes.head())  # Print the first few rows of the nodes DataFrame
gdf_nodes

gdf_relationships.plot(markersize=0.01, linewidth=0.5)
print(gdf_relationships.head()) 
gdf_relationships
