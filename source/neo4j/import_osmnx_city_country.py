import osmnx as ox
import matplotlib as mp

# Search OpenStreetMap and create a OSMNx graph
class Load_Graph:
    def __init__(self,city,country,network_type):
        self.city = city
        self.country = country
        self.network_type = network_type
    
    def load_graph_from_place(self):
        self.G = ox.graph_from_place(f"{self.city}, {self.country}", network_type=self.network_type)
        #fig, ax = ox.plot_graph(self.G)

    def load_geo_dataframe(self):
        gdf_nodes, gdf_relationships = ox.graph_to_gdfs(self.G)
        gdf_nodes.reset_index(inplace=True)
        gdf_relationships.reset_index(inplace=True)
           
        gdf_nodes.plot(markersize=0.1)
        gdf_relationships.plot(markersize=0.01, linewidth=0.5)

        return gdf_nodes, gdf_relationships
        

