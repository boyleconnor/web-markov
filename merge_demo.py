import os
from models.text_merger import TextMerger
from utils import user_input, color, split


DEFAULTS = {
    'n': 5,
    'source_one': 'frankenstein.txt',
    'source_two': 'trump.txt',
    'erratic_iterations': 1000
}


if __name__ == '__main__':
    print('Choose source #1')
    source_path_one = user_input.get_source_path(default_source=DEFAULTS['source_one'])
    source_one = open(source_path_one)

    print('Choose source #2')
    source_path_two = user_input.get_source_path(default_source=DEFAULTS['source_two'])
    source_two = open(source_path_two)

    n = user_input.get_n(default_n=DEFAULTS['n'])

    model = TextMerger(n, source_one, source_two)

    while True:
        command = input('Input a command: ')

        if command in {'e', 'erratic'}:
            iterations = user_input.get_iterations(default_iterations=DEFAULTS['erratic_iterations'])
            sequence_properties = []

            for i in range(iterations):
                sequence = model.random_sequence()
                properties = model.get_properties(*sequence)
                sequence_properties.append((sequence, properties))

            sequence, properties = max(sequence_properties, key=split.erraticity)
            print(color.colored_text(sequence, properties['biases']))

        elif command in {'t': 'text'}:
            sequence = model.random_sequence()
            properties = model.get_properties(*sequence)
            print(color.colored_text(sequence, properties['biases']))

        elif command in {'quit', 'exit', 'q'}:
            break

        elif command in {'help', 'h', '?'}:
            print('"t" or "text" to probabilistically generate a text from the combined model.')
            print('"e" or "erratic" to generate an optimally erratic text.')
            print('"h" or "help" to see this help screen')
            print('"q" or "quit" to quit')

        else:
            print('Command not recognized. Input "h" for help.')
