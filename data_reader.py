import csv
from collections import OrderedDict

def read_training_data(filename='data/train.csv'):
    return TrainingData().read(filename)

class TrainingData(object):

    def __init__(self, nodes=None, edges=None, node_attr_map=None, edge_attr_map=None):
        # List of edges
        self.nodes = nodes or []
        self.edges = edges or []
        # Node to attribute dictionary
        self.node_attr_map = node_attr_map or OrderedDict()
        self.edge_attr_map = edge_attr_map or OrderedDict()

    def read(self, filename):
        with open(filename) as f:
            r = csv.reader(f)
            header = r.next()
            choice = 1 if 'Choice' in header else 0
            keys_A = [k[2:] for k in header if k.startswith('A')]
            keys_B = [k[2:] for k in header if k.startswith('B')]
            assert keys_A == keys_B
            pivot = choice + len(keys_A)
            def insert(row):
                key = ','.join([str(i) for i in row])
                self.node_attr_map[key] = OrderedDict(zip(keys_A, row))
                return key
            for row in r:
                key_A = insert(row[choice:pivot])
                key_B = insert(row[pivot:])

                # The edge goes from the more to the less influential person
                key = (key_B, key_A) if choice and row[0] == 1 else (key_A, key_B)
                self.edges.append(key)
                self.edge_attr_map[key] = OrderedDict({'Choice': row[0] if choice else None})
        return self.rename_nodes()

    def write(self, filename):
        with open(filename, 'w') as f:
            # Construct header
            node_keys = self.node_attr_map[0].keys()
            edge_keys = self.edge_attr_map[self.edges[0]].keys()
            header = edge_keys + ['A_' + k for k in node_keys] + ['B_' + k for k in node_keys]
            r = csv.writer(f)
            r.writerow(header)
            def extract_node(key):
                return self.node_attr_map[key].values()
            def extract_edge(key):
                return self.edge_attr_map[key].values()
            for key in self.edges:
                edge = extract_edge(key)
                A, B = key if edge[0] == 0 else reversed(key)
                r.writerow(edge + extract_node(A) + extract_node(B))

    def rename_nodes(self):
        ''' Rename the dictionary keys from str -> int '''
        # Map the dictionary keys to ints
        str2int = OrderedDict((k, i) for i, k in enumerate(self.node_attr_map.keys()))
        self.nodes = range(len(self.node_attr_map))
        self.edges = [(str2int[a], str2int[b]) for a, b in self.edges]
        self.node_attr_map = OrderedDict((str2int[k], v) for k, v in self.node_attr_map.items())
        self.edge_attr_map = OrderedDict(((str2int[a], str2int[b]), v) for (a, b), v in self.edge_attr_map.items())

        return self.nodes, self.edges, self.node_attr_map
