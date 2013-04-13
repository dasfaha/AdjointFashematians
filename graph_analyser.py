import csv 
import networkx as nx
import matplotlib.pyplot as plt


edges = [] 
nodes = []

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

        personA = str(personA).replace(" ", "")
        personB = str(personB).replace(" ", "")

        nodes.append(personA)
        nodes.append(personB)

        if rank == 0:
            edges.append((personA, personB))
        else:
            edges.append((personB, personA))

        nb_rows += 1


# Make sure that we only have unique nodes
nodes = list(set(nodes))

def edges_names_to_ints(nodes, edges):
    return [(nodes.index(a), nodes.index(b)) for a, b in edges]

edges = edges_names_to_ints(nodes, edges)
edges = ["%s %s" % (str(a), str(b)) for a, b in edges]

print "Number of duplicates in csv file: %i" % (len(edges) - len(list(set(edges))))

G = nx.parse_edgelist(edges, nodetype = str)
print "Number of nodes: %i." % len(G.nodes())
print "Number of edges: %i." % len(G.edges())
nx.draw(G)
nx.draw_graphviz(G)
nx.write_dot(G,'file.dot')
