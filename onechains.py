import re
from random import randint


class Graph:
    '''
    Directional, weighted graph whose nodes are strings, and whose edge weights
    are integers.
    '''
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_node(self, node):
        '''
        Assumes <node> has not already been added to this graph
        '''
        self.nodes.add(node)

    def add_edge(self, node_one, node_two):
        '''
        Adds an edge from node_one to node_two if none exists, otherwise
        increment the weight of the existing one
        '''
        # Sanity check
        assert node_one in self.nodes and node_two in self.nodes

        if node_one in self.edges:
            if node_two in self.edges[node_one]:
                self.edges[node_one][node_two] += 1 # = self.edges[node_one][node_two] + 1
            else:
                self.edges[node_one][node_two] = 1
        else:
            # Create new adjacency table for node_one
            self.edges[node_one] = {node_two: 1}

    def get_nodes(self):
        return self.nodes

    def get_neighbors(self, node):
        return self.edges[node]

chains = Graph()

START_TOKEN = '<START>'
END_TOKEN = '<END>'
DATA_FILE = "Tweet Databases/tweetDatabase_Trump"

with open(DATA_FILE) as f:
    text = ''
    count = 0
    for line in f:
        count += 1
        tokens = re.findall('[^\]\[]+', line)
        text += START_TOKEN+' '+tokens[1]+' '+END_TOKEN+'\n'

tokens = text.split()
for i in range(len(tokens)-1):
    chains.add_node(tokens[i])
    chains.add_node(tokens[i+1])
    chains.add_edge(tokens[i], tokens[i+1])


# def gen_text(graph, max_length=100):
#     node = START_TOKEN
#     text = ''
#     count = 0
#     while node != END_TOKEN and count < max_length:
#         count += 1
#         if node != START_TOKEN:
#             text += node+' '
#         children = graph.get_neighbors(node)
#         total_weight = 0
#         die = []
#         for child, weight in children.items():
#             die += [child] * weight
#             total_weight += weight
#         node = die[randint(0, total_weight-1)]
#     return text+' '
#
#
# while True:
#     command = input('Input a command: ')
#     if command in {'edges', 'e'}:
#         node = input('edges from node: ')
#         try:
#             print(chains.get_neighbors(node))
#         except KeyError:
#             print('Node %s not in chains' % node)
#     elif command in {'nodes', 'n'}:
#         print(chains.get_nodes())
#     elif command in {'text', 't'}:
#         max_length = input('maximum length: ')
#         print(gen_text(chains))
#     elif command in {'quit', 'exit', 'q'}:
#         break
#     else:
#         print('Command not recognized')
