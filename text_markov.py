import re
from markov import Markov


class TextMarkov(Markov):
    def __init__(self, n):
        '''Initialize an n-gram based markov model specifically made for
        handling text(s).

        Inputted text will be split into n-grammable tokens using the tokenize
        function (which is saved to the object as a method).
        '''

        super().__init__(n)

    def tokenize(self, text):
        '''Convert text into tokens, including n-1 empty strings at the start
        of the text/token string (indicating start of text), and one empty
        string at the end, indicating end of text.

        Excepting start and end of text, tokens are either words (as defined by
        \w in regex) or everything between two words.
        '''
        prefix_length = self.n - 1

        return [''] * prefix_length + re.findall(r'\w+|\W+', text) + ['']

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

        tokens =  self.tokenize(text)

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
