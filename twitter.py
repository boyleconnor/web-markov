import re


def read_tweets_from_file(text_file_path):
    '''Takes path to file of tweets, returns a list of the body of those
    tweets. The file should be formatted as follows:
    
    [HANDLE][TWEET_BODY1]
    [HANDLE][TWEET_BODY2]
    [HANDLE][TWEET_BODY3]
    ...
    [HANDLE][TWEET_BODY4]
    '''
    with open(text_file_path) as text_file:
        tweets = []
        for line in text_file:
            tokens = re.findall('[^\]\[]+', line)
            tweets.append(tokens[1])
    return tweets
