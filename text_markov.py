import re
from markov import Markov


class TextMarkov(Markov):
    def __init__(self, n, tokenize=None):
        '''Initialize an n-gram based markov model specifically made for
        handling text(s).

        Inputted text will be split into n-grammable tokens using the tokenize
        function (which is saved to the object as a method).
        '''

        super().__init__(n)

        if tokenize is None:
            self.tokenize = lambda text: re.findall(r'\w+|\W+', text)
        else:
            self.tokenize = tokenize

    def read_text(self, text):
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

        tokens = [''] * prefix_length + self.tokenize(text) + ['']

        for i in range(len(tokens) - prefix_length):
            ngram = tokens[i:i+self.n]
            self.add_ngram(*ngram)

    def random_text(self, *prefix):
        '''Probabilistically generate a text. Walk through the model starting
        at recorded beginnings of texts (i.e. the prefix [''] * n-1) and ending
        at the recorded endings of texts (i.e. the suffix '').
        '''
        text = ''

        if len(prefix) == 0:
            prefix = ('',) * (self.n - 1)
        elif len(prefix) != self.n - 1:
            raise KeyError("Bad prefix length: %d" % (len(prefix),))

        while True:
            suffix = self.random_suffix(*prefix)
            if suffix == '':
                return text
            text += suffix
            prefix = prefix[1:] + (suffix,)  # FIXME: This might be inefficient for very large values of n
