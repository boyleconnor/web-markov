import argparse
from server.server import Server
from server.views import router


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Load and serve markov models')
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=str)
    args = parser.parse_args()

    server = Server(args.config_file, router)
    server.run()
