import nchains

DATA_FILE = "tweet_databases/tweetDatabase_Trump" #Choose a tweet file from tweet_databases to generate tweets that resemble those of a specific user
network = nchains.gen_graph(nchains.read_text(DATA_FILE), 2) #In this case 2-chaining is used
tweet_nodes = nchains.gen_random_path(network)
print(tweet_nodes)
tweet_network = []
for i in range(0,len(tweet_nodes)-1):
    neighbors = network.get_children(tweet_nodes[i])
    for y in neighbors:
        if (i <= len(tweet_nodes)-3 and y==tweet_nodes[i+1]): #Adds the Blue label to designate the tweet path on Mathematica
            node_tuple = tweet_nodes[i]
            node = ' '.join(node_tuple)
            connected_neighbor = ' '.join(y)
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + 'Blue-'+ str(weight_edge) + '}'
            tweet_network.append(connection_str)
        else:
            node_tuple = tweet_nodes[i]
            node = ' '.join(node_tuple)
            connected_neighbor = ' '.join(y)
            weight_edge = neighbors[y]
            connection_str = '{"' + node + '"->"' + connected_neighbor + '",' + str(weight_edge) + '}'
            tweet_network.append(connection_str)

dbase = open("NetworkBuilder/tweet_path_mathematica",'w')
dbase.write("GraphPlot[{")
Mathematica_Formula = ""
for x in tweet_network:
    Mathematica_Formula = Mathematica_Formula + x + ','
dbase.write(Mathematica_Formula[:-1]) #remove the comma at the end of the formula
dbase.write("},VertexLabeling -> True]")