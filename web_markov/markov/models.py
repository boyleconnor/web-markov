import random
import re
from collections import deque
from django.db import models
from django.conf import settings
from picklefield.fields import PickledObjectField


class Source(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    file = models.FileField(upload_to='sources/')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True  # FIXME: Null is allowed solely for testing purposes
    )

    def __str__(self):
        return self.name


class Markov(models.Model):
    WORD_NOT = '\w+|\W+'
    CHAR_BY_CHAR = '.'
    TOKENIZER_CHOICES = [
        (WORD_NOT, 'Word-Not'),
        (CHAR_BY_CHAR, 'Characters')
    ]
    name = models.CharField(max_length=100, blank=False, unique=True)
    tokenizer = models.CharField(max_length=300, choices=TOKENIZER_CHOICES, default=WORD_NOT)
    n = models.PositiveSmallIntegerField(default=5)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        null=True  # FIXME: Just for testing, don't allow null in production
    )
    graph = PickledObjectField(default=dict)

    def _add_ngram(self, prefix, suffix, weight=1):
        '''Record the occurrence of the given n-gram.
        '''
        if prefix not in self.graph:
            self.graph[prefix] = {suffix: weight}
        elif suffix not in self.graph[prefix]:
            self.graph[prefix][suffix] = weight
        else:
            self.graph[prefix][suffix] += weight

    def _tokenize(self, text):
        return re.findall(self.tokenizer, text)

    def read_text(self, text, weight=1):
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

        tokens = (prefix_length * ['']) + self._tokenize(text) + ['']

        for i in range(len(tokens) - prefix_length):
            prefix = ''.join(tokens[i:i+prefix_length])
            suffix = tokens[i+prefix_length]
            self._add_ngram(prefix, suffix, weight)

    def get_suffixes(self, prefix):
        '''For a given prefix, get a mapping of suffixes to probabilities (i.e.
        relative weights, as a fraction of 1).
        '''
        total_weight = sum(self.graph[prefix].values())
        return {suffix: (weight / total_weight) for (suffix, weight) in self.graph[prefix].items()}

    def random_suffix(self, prefix):
        '''Return a random suffix for the given prefix; probability weighted
        according to number of recorded occurrences.
        '''
        suffixes = self.get_suffixes(prefix)

        threshhold = random.random()  # 0.0 < n < 1.0

        up_to = 0.0
        for suffix, probability in suffixes.items():
            up_to += probability
            if up_to >= threshhold:
                return suffix

    def random_sequence(self):
        '''Probabilistically generate a sequence of tokens. Walk through the
        model starting at recorded beginnings of texts (i.e. the prefix [''] *
        n-1) and ending at the recorded endings of texts (i.e. the suffix '').
        '''
        prefix_length = self.n - 1
        sequence = [''] * (prefix_length)
        prefix = deque(sequence, maxlen=prefix_length)

        while True:
            prefix_string = ''.join(prefix)
            suffix = self.random_suffix(prefix_string)
            sequence.append(suffix)
            prefix.append(suffix)
            if suffix == '':
                return sequence

    def random_text(self):
        '''Probabilistically generate a text. Walk through the model starting
        at recorded beginnings of texts (i.e. the prefix [''] * n-1) and ending
        at the recorded endings of texts (i.e. the suffix '').
        '''

        sequence = self.random_sequence()
        return ''.join(sequence)

    def __str__(self):
        return self.name


class Training(models.Model):
    markov = models.ForeignKey(Markov, on_delete=models.CASCADE, related_name='trained_on')
    source = models.ForeignKey(Source, on_delete=models.CASCADE)
    weight = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ['markov', 'source']

    def _train_model(self):
        self.source.file.close()
        self.source.file.open(mode='r')
        for line in self.source.file:
            self.markov.read_text(line)

    def save(self, *args, **kwargs):
        # Actually train the model
        if self.pk is None:
            self._train_model()
        return super().save(*args, **kwargs)
