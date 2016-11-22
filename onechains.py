import re
from random import randint
from graph import Graph



START_TOKEN = '<START>'
END_TOKEN = '<END>'

def read_text(text_file_path):
    with open(text_file_path) as text_file:
        text = ''
        count = 0
        for line in text_file:
            count += 1
            tokens = re.findall('[^\]\[]+', line)
            text += START_TOKEN+' '+tokens[1]+' '+END_TOKEN+'\n'
    return text

def gen_graph(text):
    chains = Graph()
    tokens = text.split()
    for i in range(len(tokens)-1):
        chains.add_node(tokens[i])
        chains.add_node(tokens[i+1])
        chains.add_edge(tokens[i], tokens[i+1])
    return chains


def gen_random_text(graph, max_length=100):
    '''
    Return an array of tokens (words) that are statistically likely given the
    Markov Chains stored in <graph>
    '''
    node = START_TOKEN
    text = []
    count = 0
    while node != END_TOKEN and count <= max_length:
        count += 1
        if node != START_TOKEN:
            text += [node]
        children = graph.get_neighbors(node)
        total_weight = 0
        die = []
        for child, weight in children.items():
            die += [child] * weight
            total_weight += weight
        node = die[randint(0, total_weight-1)]
    return text

if __name__ == '__main__':
    DATA_FILE = "Tweet Databases/tweetDatabase_Trump"
    text = read_text(DATA_FILE)
    chains = gen_graph(text)
    while True:
        command = input('Input a command: ')
        if command in {'edges', 'e'}:
            node = input('edges from node: ')
            try:
                print(chains.get_neighbors(node))
            except KeyError:
                print('Node %s not in chains' % node)
        elif command in {'nodes', 'n'}:
            print(chains.get_nodes())
        elif command in {'text', 't'}:
            max_length = int(input('maximum length: '))
            text = gen_random_text(chains, max_length)
            print(' '.join(text))
        elif command in {'quit', 'exit', 'q'}:
            break
        else:
            print('Command not recognized')
