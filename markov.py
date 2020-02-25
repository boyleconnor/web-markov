import random
import re


class Markov:
    '''Graph-based N-Gram Markov Model
    '''
    def __init__(self, n):
        if type(n) != int:
            raise TypeError("N-gram length must be an integer")
        elif n < 2:
            raise ValueError("N-gram length must be at least 2")
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

    def random_suffix(self, *prefix):
        threshhold = random.random()
        upto = 0.0
        for suffix, probability in self.get_suffixes(*prefix).items():
            upto += probability
            if upto >= threshhold:
                return suffix

    def random_ngram(self, *prefix):
        suffix = self.random_suffix(*prefix)
        return prefix + (suffix,)
