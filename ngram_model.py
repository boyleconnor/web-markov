import random
import re


class NGram:
    '''Graph-based N-Gram Markov Model
    '''
    def __init__(self, n):
        self.n = n
        self.graph = {}

    def add_ngram(self, *ngram):
        '''Add instance of ngram to model
        e.g.

        ngram.add_ngram('hello', 'there', 'world!')

        would increase the probability of "world!" appearing after "hello" and
        "there" (where ngram is an instance of NGram such that n = 3)
        '''
        if len(ngram) != self.n:
            raise ValueError("ngram input must be of length: %d" % (self.n,))

        source = ngram[:-1]
        destination = ngram[-1]

        # Cases:

        # Source has never been recorded
        if source not in self.graph:
            self.graph[source] = {destination: 1}

        # Source has been recorded, but not preceding destination
        elif destination not in self.graph[source]:
            self.graph[source][destination] = 1

        # Source has been recorded, leading to destination
        else:
            self.graph[source][destination] += 1

    def get_suffixes(self, *prefix):
        '''Return mapping of suffixes to probabilities for a given prefix.

        "prefix" is the first n-1 elements of the ngram, "suffix" is the last
        element of the ngram.
        '''
        if len(prefix) != self.n - 1:
            raise ValueError("prefix must be of length: %d" % (self.n-1,))

        if prefix not in self.graph:
            raise KeyError("prefix %s is not the start of an ngram" % (prefix,))

        mapping = {}
        total_weight = sum(self.graph[prefix].values())
        for suffix, weight in self.graph[prefix].items():
            mapping[suffix] = weight / total_weight
        return mapping

    def get_ngrams(self, *prefix):
        '''Return map of ngrams to probabilites (between 0.0 and 1.0) for the
        given prefix (the first n-1 tokens of an ngram).
        '''
        suffix_mapping = self.get_suffixes(*prefix)
        ngram_mapping = {}
        for suffix, probability in suffix_mapping.items():
            ngram_mapping[prefix+(suffix,)] = probability
        return ngram_mapping

    def random_ngram(self, *prefix):
        threshhold = random.random()
        upto = 0.0
        for ngram, probability in self.get_ngrams(*prefix).items():
            upto += probability
            if upto >= threshhold:
                return ngram

    def read_text(self, text, tokenize=None):
        '''Read a text as a series of ngrams. This method treats the beginning
        of a text as (n-1) blank tokens (i.e. [""] * n-1) and the end of text
        as a single blank token. Texts can be any number of tokens in length
        (i.e. a text does NOT need to have a minimum of n tokens).

        An inputted text will be tokenized using the callback tokenize. If no
        tokenize function is provided, the text will be split along word
        boundaries (i.e. the punctuation and whitespace between any two words
        is grouped together as one token).
        '''
        prefix_length = self.n - 1

        if tokenize is None:
            tokenize = lambda x: re.findall(r'\w+|\W+', x)

        tokens = [''] * prefix_length + tokenize(text) + ['']

        for i in range(len(tokens) - prefix_length):
            ngram = tokens[i:i+self.n]
            self.add_ngram(*ngram)

