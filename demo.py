import os
from text_markov import TextMarkov
from twitter import read_tweets_from_file


TWEET_DB_DIR = 'tweet_databases'


def get_handle():
    file_names = os.listdir(TWEET_DB_DIR)
    print("Available Twitter handles: " + ', '.join(file_names))
    while True:
        handle = input("Please input a Twitter handle: ")
        if handle in file_names:
            return handle


def get_n():
    while True:
        try:
            n = int(input('Input n-gram size: '))
            if n < 2:
                raise ValueError()
        except ValueError:
            print("n must be an integer greater than 1")
        else:
            return n


if __name__ == '__main__':
    tweet_file = os.path.join(TWEET_DB_DIR, get_handle())
    tweets = read_tweets_from_file(tweet_file)
    model = TextMarkov(get_n())
    for tweet in tweets:
        model.read_text(tweet)

    while True:
        command = input('Input a command: ')

        if command in {'tweet', 't'}:
            tweet = model.random_text()
            print(tweet)

        elif command in {'quit', 'exit', 'q'}:
            break

        elif command in {'help', 'h', '?'}:
            print('"t" or "tweet" to probabilistically generate a tweet')
            print('"h" or "help" to see this help screen')
            print('"q" or "quit" to quit')

        else:
            print('Command not recognized')
