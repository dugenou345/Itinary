import osmnx as ox
import matplotlib as mp

Graph = ox.graph_from_place("San Mateo, CA, USA", network_type= "drive")

fig, ax = ox.plot_graph(Graph)