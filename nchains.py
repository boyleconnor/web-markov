import re
import random
import sys
from graph import Graph



START_TOKEN = '<START>'
END_TOKEN = '<END>'


if sys.version_info[0] != 3:
    print("This program requires Python 3. You are currently using:\n%s" % (sys.version,))
    exit()


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


def gen_random_path(graph, max_length=100):
    '''
    Return an array of nodes that are statistically likely given the Markov
    Chains stored in <graph>
    '''
    node = (START_TOKEN,)
    path = []
    count = 0
    while node != END_TOKEN and count <= max_length:
        count += 1
        path += [node]
        if END_TOKEN in node:
            break
        children = graph.get_children(node)
        total_weight = 0
        die = []
        for child, weight in children.items():
            die += [child] * weight
            total_weight += weight
        node = random.choice(die)
    return path


def gen_random_text(graph, max_length):
    '''
    Return a string of at most length <max_length> that is statistically likely
    given the Markov Chains stored in <graph>
    '''
    MAX_COUNTS = 1000 # Maximum number of attempts at a path before giving up
    count = 0
    while True:
        count += 1
        path = gen_random_path(graph, max_length)
        words = [node[-1] for node in path[1:-1]]
        text = ' '.join(words)
        if (len(text) <= max_length and len(text) > 0) or max_length <= 0:
            return text
        if count == MAX_COUNTS:
            print('%s PATHS ATTEMPTED, NONE FIT LENGTH RESTRICTION OF %s' % (count, max_length))
            return ''


if __name__ == '__main__':
    DATA_FILE = "tweet_databases/tweetDatabase_Trump"

    while True:
        try:
            ngram_size = int(input('Pick n-gram size: '))
            break
        except ValueError:
            print('Please pick an integer n-gram size')

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
            DEFAULT_MAX_LENGTH = 140
            while True:
                try:
                    max_length = input('maximum length (default 140): ')
                    if max_length == '':
                        max_length = 140
                    else:
                        max_length = int(max_length)
                    break
                except ValueError:
                    print('Please input an integer length or nothing')
            text = gen_random_text(chains, max_length)
            print(text)

        elif command in {'quit', 'exit', 'q'}:
            break
        else:
            print('Command not recognized')
