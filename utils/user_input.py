import os


SOURCE_DIR = 'sources'


def get_n(default_n):
    while True:
        try:
            n = input('Input n-gram size (default = %d): ' % (default_n,))
            if n == '':
                return default_n
            n = int(n)
            if n < 2:
                raise ValueError()
        except ValueError:
            print("n must be an integer greater or equal to 2")
        else:
            return n


def get_iterations(default_iterations):
    while True:
        try:
            n = input('Input number of iterations (default = %d): ' % (default_iterations,))
            if n == '':
                return default_iterations
            n = int(n)
            if n < 1:
                raise ValueError()
        except ValueError:
            print("iterations must be an integer greater or equal to 1")
        else:
            return n


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
