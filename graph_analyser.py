import networkx as nx
import matplotlib.pyplot as plt
from data_reader import TrainingData
import knn_model


class TrainingGraph:
    def __init__(self):
        self.td = TrainingData()
        self.td.read("data/train.csv")

        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.td.nodes)
        self.G.add_edges_from(self.td.edges)

    def print_stats(self):
        print "Number of nodes: %i." % len(self.G.nodes())
        print "Number of edges: %i." % len(self.G.edges())

    def print_connections(self):
        print "Degree: ", nx.degree(self.G)
        print "Graph connection: ", nx.connected_components(self.G)

    def save_dot(self):
        nx.draw(self.G)
        nx.draw_graphviz(self.G)
        nx.write_dot(self.G, 'train.dot')

    def get_influence(self, nodea, nodeb):
        ''' Returns a positive number if "nodea is more dominant than nodeb"; 
            Returns a negative number if "nodeb is more dominant than nodea";
            Returns None if no influence comparison could be performed '''

        try:
            ab = nx.shortest_path(self.G, nodea, nodeb)
        except nx.NetworkXError:
            print "Could not find one of the nodes in the graph"
            return None
        except nx.NetworkXNoPath:
            ab = None 

        try:
            ba = nx.shortest_path(self.G, nodeb, nodea)
        except nx.NetworkXError:
            print "Could not find one of the nodes in the graph"
            return None
        except nx.NetworkXNoPath:
            ba = None 

        if ab != None and ba != None: 
            if len(ab) > len(ba):
                ab = None
            else:
                ba = None

        if ab != None: 
            print "Found a path of length %i from A -> B" % len(ab)
            return 1./(len(ab))
        elif ba != None: 
            print "Found a path of length %i from B -> A" % len(ba)
            return -1./len(ba)
        else:
            return None

    def add_graph_influence_to_attr_map(self):
        for a, b in self.td.edge_attr_map.items():
            self.td.edge_attr_map[(a, b)]['Graph influence'] = get_influence(a, b)

    #def add_node_degre_eto_attr_map(self):
    #    if a, b for self.td.node_attr_map().items():
    #        self.td.edge_attr_map[(a, b)]['Graph influence'] = get_influence(a, b)
    # def eigenvector_centrality
             
if __name__ == "__main__":
    g = TrainingGraph()
    g.print_stats()
    g.add_graph_influence_to_attr_map()

    g.td.write("data/enriched_training.csv")

