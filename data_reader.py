import csv 
import networkx as nx
import matplotlib.pyplot as plt

def read_training_data():
    # List of edges
    edges = [] 
    # List of notes
    nodes = []
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

            nodes.append(personAstr)
            nodes.append(personBstr)

            node_attr_map[personAstr] = personA
            node_attr_map[personBstr] = personB

            # The edge goes from the more to the less influential person
            if rank == 0:
                edges.append((personAstr, personBstr))
            else:
                edges.append((personBstr, personAstr))

            nb_rows += 1


    # Make sure that we only have unique nodes
    nodes = list(set(nodes))

    def rename_nodes(nodes, edges, node_attr_map):
        ''' Rename the nodes from str -> int '''
        new_nodes = range(len(nodes)) 
        new_edge = [(nodes.index(a), nodes.index(b)) for a, b in edges]
        new_map = {}
        for k, v in node_attr_map.items():
            new_map[nodes.index(k)] = v

        return new_nodes, new_edge, new_map

    nodes, edges, node_attr_map = rename_nodes(nodes, edges, node_attr_map)
    return nodes, edges, node_attr_map

