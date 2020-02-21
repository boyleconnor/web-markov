class Graph:
    '''
    Directional, weighted graph whose nodes are strings or tuples of strings,
    and whose edge weights are integers.
    '''
    def __init__(self):
        self.nodes = set()
        self.edges = {}

    def add_edge(self, node_one, node_two):
        '''
        Increments the possibility of a path from node_one to node_two
        '''
        self.nodes.add(node_one)
        self.nodes.add(node_two)

        if node_one in self.edges:
            if node_two in self.edges[node_one]:
                # Increment adjacency from node_one to node_two
                self.edges[node_one][node_two] += 1
            else:
                # Create new adjacency from node_one to node_two
                self.edges[node_one][node_two] = 1
        else:
            # Create new adjacency table for node_one,
            # populate with new adjacency to node_two
            self.edges[node_one] = {node_two: 1}

    def get_nodes(self):
        return self.nodes

    def get_children(self, node):
        '''
        Return a dict of all of the children of <node> mapped to the weight of
        the edge leading to them.
        '''
        return self.edges[node]
