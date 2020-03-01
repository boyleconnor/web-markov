from collections import deque
from text_markov import TextMarkov


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
            self.markov_one.read_text(text)

        self.markov_two = TextMarkov(n)
        for text in source_two:
            self.markov_two.read_text(text)

        self.merged_markov = TextMarkov(n)
        self.merged_markov.update(self.markov_one)
        self.merged_markov.update(self.markov_two)

    def get_bias(self, *ngram):
        '''Return a value (-1.0 <= v <= 1.0) representing the likelihood of
        finding the value in the first source minus the likelihood of finding
        it in the second source. For our purposes, if even the prefix has not
        been observed, the probability is considered 0.0.
        '''
        prefix = ngram[:-1]
        suffix = ngram[-1]
        bias = 0.0

        weights = self.markov_one.get_suffixes(*prefix)
        if suffix in weights:
            bias += weights[suffix]

        weights = self.markov_two.get_suffixes(*prefix)
        if suffix in weights:
            bias -= weights[suffix]

        return bias

    def get_properties(self, *sequence):
        '''Return a dictionary with info on the net_bias, movement, and
        bias-by-token of the sequence.
        '''
        prefix_length = self.n - 1
        start_of_text = ('',) * prefix_length

        ngram = deque(start_of_text, self.n)
        biases = [0.0] * prefix_length
        movement = 0.0
        net_bias = 0.0
        previous_bias = 0.0
        total_bias = 0.0
        for i in range(prefix_length, len(sequence)):
            ngram.append(sequence[i])
            bias = self.get_bias(*ngram)
            biases.append(bias)
            net_bias += bias
            total_bias += abs(bias)
            movement += abs(bias - previous_bias)
            previous_bias = bias
        return {'biases': biases, 'net_bias': net_bias, 'movement': movement, 'total_bias': total_bias}

    def random_sequence(self):
        '''Return a sequence generated from a probabilistic walk through the
        graph starting with start-of-text and ending with end-of-text.
        '''
        prefix_length = self.n - 1
        start_of_text = ('',) * prefix_length
        sequence = self.merged_markov.random_sequence(*start_of_text)
        return sequence
