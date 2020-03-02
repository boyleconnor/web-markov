import os
from models.text_markov import TextMarkov
from utils import user_input


DEFAULTS = {
    'n': 5,
    'source': 'frankenstein.txt'
}


if __name__ == '__main__':
    source_path = user_input.get_source_path(default_source=DEFAULTS['source'])
    source_file = open(source_path)

    model = TextMarkov(user_input.get_n(default_n=DEFAULTS['n']))

    for line in source_file:
        model.read_text(line.strip('\n'))

    while True:
        command = input('Input a command: ')

        if command in {'text', 't'}:
            print(model.random_text())

        elif command in {'quit', 'exit', 'q'}:
            break

        elif command in {'help', 'h', '?'}:
            print('"t" or "text" to probabilistically generate a text.')
            print('"h" or "help" to see this help screen')
            print('"q" or "quit" to quit')

        else:
            print('Command not recognized. Input "h" for help.')
