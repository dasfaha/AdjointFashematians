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

    def add_graph_influence(self):
        for a, b in self.td.edge_attr_map.items():
            self.td.edge_attr_map[(a, b)]['Graph influence'] = get_influence(a, b)

    def add_node_degree(self):
        in_degrees = self.G.in_degree()
        out_degrees = self.G.out_degree()

        for i in self.td.node_attr_map.keys():
            self.td.node_attr_map[i]['Node in-degree'] = in_degrees[i]
            self.td.node_attr_map[i]['Node out-degree'] = out_degrees[i]

    def add_eigenvector_centrality(self):
        ec = nx.eigenvector_centrality(self.G)

        for i in self.td.node_attr_map.keys():
            self.td.node_attr_map[i]['Eigenvector centrality'] = ec[i]

    def add_page_rank(self):
        pr = nx.pagerank(self.G)

        for i in self.td.node_attr_map.keys():
            self.td.node_attr_map[i]['Page rank'] = pr[i]

             
if __name__ == "__main__":
    g = TrainingGraph()
    g.print_stats()
    g.add_graph_influence()
    g.add_node_degree()
    g.add_eigenvector_centrality()
    g.add_page_rank()

    g.td.write("data/enriched_training.csv")

