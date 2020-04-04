import re
import sys
import time
from multiprocessing import Pool, Queue
from functools import reduce


def word_not(line):
    return re.findall('\w+|\W+', line)


def line_to_graph(args):
    tokens, n = args
    graph = {}
    prefix_length = n - 1
    for i in range(prefix_length, len(tokens)):
        prefix = tokens[i-prefix_length:i]
        suffix = tokens[i]
        if prefix not in graph:
            graph[prefix] = {suffix: 1}
        else:
            if suffix not in graph[prefix]:
                graph[prefix][suffix] = 1
            else:
                graph[prefix][suffix] += 1
    return graph


def merge_graph(graph_one, graph_two):
    for prefix in graph_two.keys():
        for suffix in graph_two[prefix].keys():
            weight = graph_two[prefix][suffix]
            if prefix not in graph_one:
                graph_one[prefix] = {suffix: weight}
            else:
                if suffix not in graph_one[prefix]:
                    graph_one[prefix][suffix] = weight
                else:
                    graph_one[prefix][suffix] += weight
    del graph_two
    return graph_one


def source_to_graph(file_path, tokenize, process_count, n):
    with open(file_path, 'rb') as text_file:
        token_sequences = []
        for line in text_file:
            token_sequence = tuple([''] * (n-1) + word_not(line.decode()) + [''])
            token_sequences.append((token_sequence, n))
    t1 = time.time()
    with Pool(processes=process_count) as pool:
        line_graphs = pool.map(line_to_graph, token_sequences)

    full_graph = reduce(merge_graph, line_graphs)
    t2 = time.time()
    print("Processing time: ", str(t2-t1))
    return full_graph


if __name__ == '__main__':
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        process_count = int(sys.argv[2])
    else:
        process_count = 4
    source_to_graph(file_path, word_not, process_count, 5)  # FIXME: Change default n from 5

