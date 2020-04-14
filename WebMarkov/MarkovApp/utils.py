import re
import sys


def source_to_graph(source_file, tokenizer, n):
    '''Turn source_file into a markov model graph. tokenizer should be a regex
    pattern function, which turns a string into a series of 'tokens'.
    '''
    prefix_length = n-1
    graph = {}
    for line in source_file:
        tokens = tuple([''] * (n - 1) + re.findall(tokenizer, line) + [''])
        for i in range(len(tokens)-prefix_length):
            prefix = tokens[i:i+prefix_length]
            suffix = tokens[i+prefix_length]
            if prefix in graph and suffix in graph[prefix]:
                graph[prefix][suffix] += 1
            elif prefix in graph:
                graph[prefix][suffix] = 1
            else:
                graph[prefix] = {suffix: 1}
    return graph


if __name__ == '__main__':
    file_path = sys.argv[1]
    if len(sys.argv) > 2:
        n = sys.argv[2]
    else:
        n = 5
    with open(file_path) as source_file:
        print(source_to_graph(source_file, '\w+|\W+', 5))  # FIXME: Change default n from 5
