import osmnx as ox
import matplotlib as mp

# Search OpenStreetMap and create a OSMNx graph
class Load_Graph:
    def __init__(self,city,country,network_type):
        self.city = city
        self.country = country
        self.network_type = network_type
    
    def load_graph_from_place(self):
        G = ox.graph_from_place(f"{self.city}, {self.country}", network_type=self.network_type)
        fig, ax = ox.plot_graph(G)

