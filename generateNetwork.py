from graph import Graph
import re
from random import randint
import nchains

DATA_FILE = "tweet_databases/tweetDatabase_Trump"
network = nchains.gen_graph(nchains.read_text(DATA_FILE),2)
tweet_words = nchains.gen_random_text(network,50) #tweet is a list of words
print(tweet_words)
tweet_network = []
for i in range(0,len(tweet_words)-1):
    neighbors = network.get_children((tweet_words[i],tweet_words[i+1]))
    for y in neighbors:
        if (i <= len(tweet_words)-3 and y==(tweet_words[i+1],tweet_words[i+1])):
            node = tweet_words[i] + ' ' + tweet_words[i + 1]
            connected_neighbor = y[0] + ' ' + y[1]
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + 'Blue'+ str(weight_edge) + '}'
            tweet_network.append(connection_str)
        else:
            node = tweet_words[i] + ' ' + tweet_words[i + 1]
            connected_neighbor = y[0] + ' ' + y[1]
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + str(weight_edge) + '}'
            tweet_network.append(connection_str)

dbase = open("sample_tweet_words",'w')
for x in tweet_network:
    dbase.write(x)
    dbase.write(',')

