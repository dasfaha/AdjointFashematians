from graph_analyser import TrainingGraph
from math import sqrt

class GraphPredicter():

    def __init__(self):
        self.tg = TrainingGraph(remove_edges=100)

    def diff(self, a_attr, b):
        d = 0.0
        for k in self.tg.td.node_attr_map[a].keys():
            d += (float(a_attr[k])-float(self.tg.td.node_attr_map[b][k]))**2
        return sqrt(d)

    def find_closest_neighbour(self, a_attr):
        dist = [diff(a_attr, b) for b in self.tg.td.nodes] 
        mindist = min(dist)

        for i, d in enumerate(dist):
            if d == mindist:
                return i

    def predict(self, a_attr, b_attr):
        a = find_closest_neighbour(a_attr)
        b = find_closest_neighbour(b_attr)

        i = self.tg.get_influence(a, b) > 0
        return i

    def perform_test():
        correct = 0
        total = 0
        for a, b in tg.removed_edges:
            a_attr = tg.td.node_attr_map[a]
            b_attr = tg.td.node_attr_map[b]
            if predict(a_attr, b_attr) > 0:
              correct += 1
            total += 1

        print "Success ratio %f" % (float(correct)/total) 

gp = GraphPredicter()
