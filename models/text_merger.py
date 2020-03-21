from collections import deque
from .text_markov import TextMarkov


class TextMerger:
    '''A model that can train on two distinct sources of text, then generate
    probabilistic text from their combination. The TextMerger can then provide
    analyses of the produced text based on the training results from each
    distinct source.
    '''
    def __init__(self, n, source_one, source_two):
        '''source_one and source_two should each be an iterable containing a
        text.
        '''
        self.n = n

        self.markov_one = TextMarkov(n)
        for text in source_one:
            self.markov_one.read_text(text.strip('\n'))

        self.markov_two = TextMarkov(n)
        for text in source_two:
            self.markov_two.read_text(text.strip('\n'))

        self.merged_markov = TextMarkov(n)
        self.merged_markov.update(self.markov_one)
        self.merged_markov.update(self.markov_two)

    def get_bias(self, *ngram):
        '''Return a value (-1.0 <= v <= 1.0) representing the likelihood of
        finding the value in the first source minus the likelihood of finding
        it in the second source. For our purposes, if the ngram has not been
        observed at all in the opposite source, it will be regarded as p = 1.0
        in this source.
        '''
        prefix = ngram[:-1]
        suffix = ngram[-1]
        bias = 0.0

        weights_one = self.markov_one.get_suffixes(*prefix)
        weights_two = self.markov_two.get_suffixes(*prefix)

        if suffix in weights_one and suffix not in weights_two:
            return 1.0
        elif suffix not in weights_one and suffix in weights_two:
            return -1.0
        else:
            return weights_one[suffix] - weights_two[suffix]

    def get_biases(self, *sequence):
        '''Return a dictionary with info on the net_bias, movement, and
        bias-by-token of the sequence.
        '''
        prefix_length = self.n - 1
        start_of_text = ('',) * prefix_length

        ngram = deque(start_of_text, self.n)
        biases = [0.0] * prefix_length

        for i in range(prefix_length, len(sequence)):
            ngram.append(sequence[i])
            bias = self.get_bias(*ngram)
            biases.append(bias)

        return tuple(biases)

    def random_sequence(self):
        '''Return a sequence generated from a probabilistic walk through the
        graph starting with start-of-text and ending with end-of-text.
        '''
        prefix_length = self.n - 1
        start_of_text = ('',) * prefix_length
        sequence = self.merged_markov.random_sequence(*start_of_text)
        return sequence


class MergedSequence:
    def __init__(self, tokens, biases):
        if len(tokens) != len(biases):
            raise ValueError("Each token must have an associated bias")
        self.tokens = tokens
        self.biases = biases
        self.net_bias = 0.0
        self.total_bias = 0.0
        self.movement = 0.0

        previous_bias = 0.0
        for bias in biases:
            self.net_bias += bias
            self.total_bias += abs(bias)
            self.movement += abs(bias - previous_bias)
            previous_bias = bias

    def get_token_biases(self):
        '''Returns ordered collection of a (token, bias) pairs.
        '''
        return zip(tokens, biases)

    def erraticity(self):
        return self.movement - abs(self.net_bias)

    def neutrality(self):
        return len(self.tokens) - self.total_bias - abs(self.net_bias)
