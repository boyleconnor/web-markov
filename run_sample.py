import nchains
import os

#Sources:
#Iterate through files in a directory: http://stackoverflow.com/questions/10377998/how-can-i-iterate-over-files-in-a-given-directory

lst_file_names = ""
for file_name in os.listdir("tweet_databases"):
    lst_file_names = lst_file_names+file_name[14:]+','

print("Choice of users: " + lst_file_names[:-1])

user = str(input('Pick a twitter user for the bot to mimic: '))
DATA_FILE = "tweet_databases/" + user
ngram_size = int(input('Pick n-gram size (preferably from 1 to 3): '))

print("Input 'e' if you want to see the edges.")
print("Input 'n' if you want to see the nodes.")
print("Input 't' if you want to see the texts.")
print("Input 'q' if you want to quit.")

text = nchains.read_text(DATA_FILE)
chains = nchains.gen_graph(text, ngram_size)

while True:
    command = input('Input a command: ')
    if command in {'edges', 'e'}:
        node = tuple()
        for x in range(ngram_size):
            token = input("token %s: " % (x + 1))
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
        text = nchains.gen_random_text(chains, max_length)
        print(text)

    elif command in {'quit', 'exit', 'q'}:
        break
    else:
        print('Command not recognized')
