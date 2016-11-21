from graph import Graph
from onechains import gen_text
import re
from random import randint

network = Graph()

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
    network.add_node(tokens[i])
    network.add_node(tokens[i+1])
    network.add_edge(tokens[i], tokens[i+1])

tweet_words = gen_text(network)
print(tweet_words)
tweet_network = []
for x in tweet_words:
    neighbors = network.get_neighbors(x)
    for y in neighbors:
        node = x
        connected_neighbor = y
        weight_edge = neighbors[y]
        connection_str = '{"'+node+'"->"'+connected_neighbor+'",'+str(weight_edge)+'}'
        tweet_network.append(connection_str)

dbase = open("sample_tweet_words",'w')
for x in tweet_network:
    dbase.write(x)
    dbase.write(',')

