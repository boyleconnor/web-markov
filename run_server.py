import argparse
import sys
from server.server import Server
from server.views import router


if __name__ == '__main__':
    if sys.version_info[0] != 3:
        print("This script and package require Python 3")
        exit()

    parser = argparse.ArgumentParser(description='Load and serve markov models')
    parser.add_argument('config_file', metavar='CONFIG_FILE', type=str)
    args = parser.parse_args()

    server = Server(args.config_file, router)
    server.run()
