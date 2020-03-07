import os


SOURCE_DIR = 'sources'


def get_integer(default_value, name, minimum):
    while True:
        try:
            number = input('Input %s (default = %d): ' % (name, default_value,))
            if number == '':
                return default_value
            number = int(number)
            if number < minimum:
                raise ValueError()
        except ValueError:
            print("Input must be an integer greater or equal to %d" % (minimum,))
        else:
            return number


def get_n(default_n):
    return get_integer(default_n, 'n-gram size', 2)


def get_iterations(default_iterations):
    return get_integer(default_iterations, 'number of iterations', 1)


def get_sample_size(default_sequences):
    return get_integer(default_sequences, 'sample size', 1)


def get_source_path(default_source):
    source_files = os.listdir(SOURCE_DIR)
    while True:
        print('Available text sources: ')
        print(', '.join(source_files))
        source_path = input('Select source (default = %s): ' % (default_source,))
        if source_path == '':
            return os.path.join(SOURCE_DIR, default_source)
        elif source_path in source_files:
            return os.path.join(SOURCE_DIR, source_path)
        else:
            print('%s is not a valid source file.' % (source_path,))
