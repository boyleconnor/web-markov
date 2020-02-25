from text_markov import TextMarkov


def print_help():
    print()
    print('"v" or "verse" to generate a random verse')
    print('"h" or "help" to view this help text')
    print('"q" or "quit" to quit')
    print()

model = TextMarkov(5)
bible = open('books/bible.txt')

print('Loading Bible...')
for line in bible.readlines():
    model.read_text(line.strip('\n'))
print('Bible loaded succesfully.')

print_help()

while True:
    command = input('Input command: ')
    if command in {'v', 'verse'}:
        print()
        print(model.random_text())
        print()
    elif command in {'h', '?', 'help'}:
        print_help()
    elif command in {'q', 'quit', 'exit'}:
        exit()
    else:
        print()
        print("Not a valid command. Input 'h' for help.")
        print()
