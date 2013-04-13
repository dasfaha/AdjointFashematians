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

if __name__ == "__main__":
    g = TrainingGraph()
    g.print_stats()

