import re
import random
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


def gen_graph(text, n):
    '''
    Generate a graph of n-grams from the text
    '''
    if n < 1:
        raise ValueError("n must be greater than or equal to 1")
    elif type(n) != int:
        raise TypeError("n must be an integer")
    chains = Graph()
    lines = text.split('\n')
    for line in lines:
        tokens = line.split()
        node = tuple()
        for x in range(n):
            try:
                new_node = node + (tokens[x],)
            except IndexError:
                break
            chains.add_edge(node, new_node)
            node = new_node
        for i in range(len(tokens)-n):
            node_one = tuple([tokens[i+j] for j in range(n)])
            node_two = tuple([tokens[i+j+1] for j in range(n)])
            chains.add_edge(node_one, node_two)
    return chains


def gen_random_text(graph, max_length=100):
    '''
    Return an array of tokens (words) that are statistically likely given the
    Markov Chains stored in <graph>
    '''
    node = (START_TOKEN,)
    text = []
    count = 0
    while node != END_TOKEN and count <= max_length:
        count += 1
        if END_TOKEN in node:
            break
        elif node != (START_TOKEN,):
            text += [node[-1]]
        children = graph.get_children(node)
        total_weight = 0
        die = []
        for child, weight in children.items():
            die += [child] * weight
            total_weight += weight
        node = random.choice(die)
    return text

if __name__ == '__main__':
    DATA_FILE = "tweet_databases/tweetDatabase_Trump"
    ngram_size = int(input('Pick n-gram size: '))
    text = read_text(DATA_FILE)
    chains = gen_graph(text, ngram_size)
    while True:
        command = input('Input a command: ')
        if command in {'edges', 'e'}:
            node = tuple()
            for x in range(ngram_size):
                token = input("token %s: " % (x+1))
                if token == '':
                    break
                node += (token,)
            try:
                children = chains.get_children(node)
                print((node, children))
            except KeyError:
                print('Node %s not in chains' % str(node))
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
