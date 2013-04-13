import networkx as nx
import matplotlib.pyplot as plt
import data_reader 


class TrainingGraph:
    def __init__(self):
        self.nodes, self.edges, self.node_attr_map = data_reader.read_training_data()

        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.nodes)
        self.G.add_edges_from(self.edges)

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

if __name__ == "__main__":
    g = TrainingGraph()
    g.print_stats()
