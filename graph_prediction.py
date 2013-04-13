from graph_analyser import TrainingGraph
from math import sqrt

class GraphPredicter():

    def __init__(self, remove_edges=100):
        self.tg = TrainingGraph(remove_edges=remove_edges)

    def diff(self, a_attr, b):
        d = 0.0
        #['follower_count','following_count','listed_count','mentions_received','retweets_received','mentions_sent','retweets_sent','posts','network_feature_1','network_feature_2','network_feature_3']
        for k in self.tg.td.node_attr_map[b].keys():
            d += (float(a_attr[k])-float(self.tg.td.node_attr_map[b][k]))**2
        return sqrt(d)

    def find_closest_neighbour(self, a_attr):
        dist = [self.diff(a_attr, b) for b in self.tg.td.nodes] 
        mindist = min(dist)

        for i, d in enumerate(dist):
            if d == mindist:
                return i

    def predict(self, a_attr, b_attr):
        a = self.find_closest_neighbour(a_attr)
        b = self.find_closest_neighbour(b_attr)

        i = self.tg.get_influence(a, b) > 0
        return i

    def perform_test(self):
        correct = 0
        total = 0
        for a, b in self.tg.removed_edges:
            a_attr = self.tg.td.node_attr_map[a]
            b_attr = self.tg.td.node_attr_map[b]
            if self.predict(a_attr, b_attr) > 0:
              correct += 1
            total += 1

        print "Success ratio %f" % (float(correct)/total) 

for i in range(1,10):
    gp = GraphPredicter(remove_edges=i*10)
    gp.perform_test()
