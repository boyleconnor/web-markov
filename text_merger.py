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

