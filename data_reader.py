import csv

def read_training_data(filename='data/train.csv'):
    return TrainingData().read(filename)

class TrainingData(object):

    def __init__(self):
        # List of edges
        self.edges = []
        # Node to attribute dictionary
        self.node_attr_map = {}

    def read(self, filename):
        with open(filename) as f:
            r = csv.reader(f)
            header = r.next()
            choice = 1 if 'Choice' in header else 0
            keys_A = [k[2:] for k in header if k.startswith('A')]
            keys_B = [k[2:] for k in header if k.startswith('B')]
            assert keys_A == keys_B
            self.keys = keys_A
            pivot = choice + len(keys_A)
            def insert(row):
                key = ','.join([str(i) for i in row])
                self.node_attr_map[key] = dict(zip(keys_A, row))
                return key
            for row in r:
                key_A = insert(row[choice:pivot])
                key_B = insert(row[pivot:])

                # The edge goes from the more to the less influential person
                if choice and row[0] == 0:
                    self.edges.append((key_A, key_B))
                else:
                    self.edges.append((key_B, key_A))
        return self.rename_nodes()

    def rename_nodes(self):
        ''' Rename the dictionary keys from str -> int '''
        # Map the dictionary keys to ints
        str2int = dict((k, i) for i, k in enumerate(self.node_attr_map.keys()))
        new_nodes = range(len(self.node_attr_map))
        new_edge = [(str2int[a], str2int[b]) for a, b in self.edges]
        new_map = dict((str2int[k], v) for k, v in self.node_attr_map.items())

        return new_nodes, new_edge, new_map
