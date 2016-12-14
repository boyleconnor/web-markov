
import nchains

DATA_FILE = "tweet_databases/tweetDatabase_elonmusk"
network = nchains.gen_graph(nchains.read_text(DATA_FILE), 2)
tweet_nodes = nchains.gen_random_path(network)
print(tweet_nodes)
tweet_network = []
for i in range(1,len(tweet_nodes)-1):
    neighbors = network.get_children(tweet_nodes[i])
    for y in neighbors:
        if (i <= len(tweet_nodes)-3 and y==tweet_nodes[i+1]):
            node_tuple = tweet_nodes[i]
            node = node_tuple[0] + ' ' + node_tuple[1]
            connected_neighbor = y[0] + ' ' + y[1]
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + 'Blue-'+ str(weight_edge) + '}'
            tweet_network.append(connection_str)
        else:
            node_tuple = tweet_nodes[i]
            node = node_tuple[0] + ' ' + node_tuple[1]
            connected_neighbor = y[0] + ' ' + y[1]
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + str(weight_edge) + '}'
            tweet_network.append(connection_str)

dbase = open("NetworkBuilder/tweet_path_mathematica",'w')
dbase.write("GraphPlot[{")
for x in tweet_network:
    dbase.write(x)
    dbase.write(',')
dbase.write("VertexLabeling -> True]")