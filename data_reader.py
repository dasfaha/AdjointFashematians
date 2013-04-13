import csv

def read_training_data():
    # List of edges
    edges = []
    # Node to attribute dictionary
    node_attr_map = {}

    with open('data/train.csv', 'rb') as csvfile:
        csvreader = csv.reader(csvfile)
        firstrow = True
        nb_rows = 0

        # Read the csv file and generate the adjacency list
        for row in csvreader:
            if firstrow:
                firstrow = False
                continue

            rank = int(row[0])

            delimiter = (len(row)-1)/2
            personA = row[1:delimiter+1]
            personB = row[delimiter+1:]

            personAstr = str(personA).replace(" ", "")
            personBstr = str(personB).replace(" ", "")

            node_attr_map[personAstr] = personA
            node_attr_map[personBstr] = personB

            # The edge goes from the more to the less influential person
            if rank == 0:
                edges.append((personAstr, personBstr))
            else:
                edges.append((personBstr, personAstr))

            nb_rows += 1


    def rename_nodes(edges, node_attr_map):
        ''' Rename the dictionary keys from str -> int '''
        # Map the dictionary keys to ints
        str2int = dict((k, i) for i, k in enumerate(node_attr_map.keys()))
        new_nodes = range(len(node_attr_map))
        new_edge = [(str2int[a], str2int[b]) for a, b in edges]
        new_map = dict((str2int[k], v) for k, v in node_attr_map.items())

        return new_nodes, new_edge, new_map

    return rename_nodes(edges, node_attr_map)

