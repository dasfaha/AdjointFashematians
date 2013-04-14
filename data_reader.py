import csv
from collections import OrderedDict

def read_training_data(filename='data/train.csv'):
    return TrainingData().read(filename)

class TrainingData(object):

    def __init__(self, nodes=None, edges=None, node_attr_map=None, edge_attr_map=None, label_map=None):
        # List of edges
        self.nodes = nodes or []
        self.edges = edges or []
        # Node to attribute dictionary
        self.node_attr_map = node_attr_map or OrderedDict()
        self.edge_attr_map = edge_attr_map or OrderedDict()
        self.label_map = label_map or OrderedDict()

    def read(self, filename, label='Choice'):
        with open(filename) as f:
            r = csv.reader(f)
            # Skip header
            header = r.next()
            # Do we have a label?
            start = 1 if label in header else 0
            # Check how many features we have
            keys_A = [k[2:] for k in header if k.startswith('A')]
            keys_B = [k[2:] for k in header if k.startswith('B')]
            assert keys_A == keys_B
            self.keys = keys_A
            pivot = start + len(keys_A)
            def insert(row):
                key = ','.join([str(i) for i in row])
                # Build a set of unique nodes
                self.node_attr_map[key] = OrderedDict(zip(keys_A, row))
                return key
            for row in r:
                key_A = insert(row[start:pivot])
                key_B = insert(row[pivot:])

                # The edge goes from the more to the less influential person
                key = (key_B, key_A) if start and row[0] == 1 else (key_A, key_B)
                self.edges.append(key)
                self.label_map[key] = row[0] if start else None
        return self.rename_nodes()

    def write(self, filename):
        with open(filename, 'w') as f:
            # Construct header
            node_keys = [k for k in self.node_attr_map[0].keys() if k not in self.keys]
            edge_keys = self.edge_attr_map[self.edges[0]].keys()
            header = edge_keys + ['A_' + k for k in node_keys] + ['B_' + k for k in node_keys]
            r = csv.writer(f)
            r.writerow(header)
            def extract_node(key):
                return [v for k, v in self.node_attr_map[key].items() if k not in self.keys]
            def extract_edge(key):
                return self.edge_attr_map[key].values()
            for key in self.edges:
                A, B = key if self.label_map[key] == 0 else reversed(key)
                r.writerow(extract_edge(key) + extract_node(A) + extract_node(B))

    def rename_nodes(self):
        ''' Rename the dictionary keys from str -> int '''
        # Map the dictionary keys to ints
        str2int = OrderedDict((k, i) for i, k in enumerate(self.node_attr_map.keys()))
        self.nodes = range(len(self.node_attr_map))
        self.edges = [(str2int[a], str2int[b]) for a, b in self.edges]
        self.node_attr_map = OrderedDict((str2int[k], v) for k, v in self.node_attr_map.items())
        self.edge_attr_map = OrderedDict((k, OrderedDict()) for k in self.edges)
        self.label_map = OrderedDict(((str2int[a], str2int[b]), v) for (a, b), v in self.label_map.items())

        return self.nodes, self.edges, self.node_attr_map
