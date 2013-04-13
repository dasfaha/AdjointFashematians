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
            print "Ops! Found a path from A -> B and one from B -> A. This is strange!"
            return 0.

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

