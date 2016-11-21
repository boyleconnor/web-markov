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
