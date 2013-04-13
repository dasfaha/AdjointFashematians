import networkx as nx
import matplotlib.pyplot as plt
import data_reader 


class TrainingGraph:
    def __init__(self):
        self.nodes, self.edges, self.node_attr_map = data_reader.read_training_data()

        # Build a edge list that is compatible with networkx 
        edgesstr = ["%s %s" % (str(a), str(b)) for a, b in self.edges]
        self.G = nx.parse_edgelist(edgesstr, nodetype = str)

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
