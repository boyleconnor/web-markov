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
