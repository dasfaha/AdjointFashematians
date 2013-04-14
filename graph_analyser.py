import networkx as nx
import matplotlib.pyplot as plt
from data_reader import TrainingData

class TrainingGraph:
    def __init__(self, filename="data/train.csv", remove_edges=0):
        self.td = TrainingData()
        self.td.read(filename)

        # remove some if the sample edges for validation purposes
        self.removed_edges = self.td.edges[len(self.td.edges)-remove_edges:]
        self.reduced_edges = self.td.edges[:len(self.td.edges)-remove_edges]

        self.G = nx.DiGraph()
        self.G.add_nodes_from(self.td.nodes)
        self.G.add_edges_from(self.reduced_edges)

    def reduce_graph_to_largest_component(self):
        ''' Reduces the graph to only the largest connected part '''
        self.G = nx.weakly_connected_component_subgraphs(self.G)[0]

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
            return 0.0
        except nx.NetworkXNoPath:
            ab = None 

        try:
            ba = nx.shortest_path(self.G, nodeb, nodea)
        except nx.NetworkXError:
            print "Could not find one of the nodes in the graph"
            return 0.0
        except nx.NetworkXNoPath:
            ba = None 

        if ab != None and ba != None: 
            if len(ab) > len(ba):
                ab = None
            else:
                ba = None

        if ab != None: 
            return 1./(len(ab))
        elif ba != None: 
            return -1./len(ba)
        else:
            return 0.0

    def add_graph_influence(self):
        for a, b in self.td.edges:
            self.td.edge_attr_map[(a, b)]['Graph influence'] = self.get_influence(a, b)

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

    def add_hits(self):
        hits = nx.hits(self.G)[0]

        for i in self.td.node_attr_map.keys():
            self.td.node_attr_map[i]['HITS'] = hits[i]

    def add_number_of_paths(self):
        for a, b in self.td.edges:
            self.td.edge_attr_map[(a, b)]['Number of paths'] = len(list(nx.all_simple_paths(self.G, a, b, cutoff=3)))

def main():
    import knn_model
    # Enrich the training file
    g = TrainingGraph(filename="data/train.csv")

    g.print_stats()
    print "*** Enriching train data ***"
    print "Computing enriched edge data"
    # Edge attributes
    #g.add_graph_influence()
    g.add_number_of_paths()
    # Handle the enriched node data
    print "Computing enriched node data"
    g.add_node_degree()
    g.add_eigenvector_centrality()
    g.add_page_rank()
    g.add_hits()

    # Enrich the test file
    print "*** Enriching test data ***"
    train_g = TrainingGraph(filename="data/test.csv")

    # Handle the enriched edge data
    print "Computing enriched edge data"
    ctr = 0 
    for a, b in train_g.td.edges:
        ctr += 1
        print "\rComputing path %i/%i." % (ctr, len(train_g.td.edges)),
        # Get the two neighbour nodes on the training graph
        test_a_attr = train_g.td.node_attr_map[a]
        neighb_a = knn_model.predict(test_a_attr)[0]

        test_b_attr = train_g.td.node_attr_map[b]
        neighb_b = knn_model.predict(test_b_attr)[0]

        avg_nb_paths = [] 
        #avg_graph_influence = [] 

        for i in range(len(neighb_a)):
            #avg_graph_influence.append(g.get_influence(neighb_a[i], neighb_b[i]))
            avg_nb_paths.append(len(list(nx.all_simple_paths(g.G, neighb_a[i], neighb_b[i], cutoff=3))))

        #train_g.td.edge_attr_map[(a, b)]['Graph influence'] = float(sum(avg_graph_influence))/len(avg_graph_influence)
        train_g.td.edge_attr_map[(a, b)]['Number of paths'] = float(sum(avg_nb_paths))/len(avg_nb_paths)

    # Handle the enriched node data
    print "\nComputing enriched node data"
    for test_node in train_g.td.nodes:
        
        test_node_attr = train_g.td.node_attr_map[test_node]
        # Get the nearest neighbour nodes on the train graph
        neighb_nodes = knn_model.predict(test_node_attr)[0]

        neighb_nodes_attr = [g.td.node_attr_map[neighb_node] for neighb_node in neighb_nodes]

        # Enrich the test data 
        for k in neighb_nodes_attr[0].keys():
            if k not in train_g.td.keys: 
                train_g.td.node_attr_map[test_node][k] = float(sum([neighb_nodes_attr[i][k] for i in range(len(neighb_nodes_attr))]))/len(neighb_nodes_attr)


    return g, train_g

if __name__ == "__main__":
    g, train_g = main()
    g.td.write("data/enriched_training.csv")
    train_g.td.write("data/enriched_test.csv")
