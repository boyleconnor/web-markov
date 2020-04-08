import random
import re
from collections import deque
from io import TextIOWrapper
from django.db import models
from .utils import source_to_graph


DEFAULT_N = 5


class Source(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    source_file = models.FileField(upload_to='sources/')

    def __str__(self):
        return self.name


class Markov(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    tokenizer = models.CharField(max_length=300, default='\w+|\W+', editable=False)
    n = models.PositiveSmallIntegerField(default=DEFAULT_N, editable=False)
    trained_on = models.ManyToManyField(Source)

    def tokenize(self, text):
        return [''] * (self.n - 1) + re.findall(self.tokenizer, text) + ['']

    def read_text(self, text):
        '''Update the markov model based on the inputted text.
        '''
        tokens = self.tokenize(text)
        for i in range(len(tokens)-(self.n-1)):
            prefix_tokens = ''.join(tokens[i:i+self.n-1])
            suffix_token = tokens[i+self.n-1]
            prefix, created = self.prefixes.get_or_create(tokens=prefix_tokens, defaults={'occurrences': 1})
            if not created:
                prefix.occurrences += 1
                prefix.save()
            suffix, created = prefix.suffixes.get_or_create(token=suffix_token, defaults={'weight': 1})
            if not created:
                suffix.weight += 1
                suffix.save()

    def train_on(self, source):
        if source in self.trained_on.all():
            raise ValueError("Markov: %s has alrady been trained on source: %s"
                    % (repr(source), str(source)))
        source_file = TextIOWrapper(source.source_file)
        print("Generating graph...")
        graph = source_to_graph(source_file, self.tokenizer, self.n)
        print("Graph generated")
        prefix_number = 0
        updated_prefixes = []
        updated_suffixes = []
        for prefix_tokens in graph:
            # prefix_number += 1
            # print("Saving prefix #%d of %d to database\r" % (prefix_number, len(graph)), end="")
            prefix_string = ''.join(prefix_tokens)
            occurrences = sum(graph[prefix_tokens].values())
            prefix, created_prefix = self.prefixes.get_or_create(tokens=prefix_string, defaults={'occurrences': occurrences})
            if not created_prefix:
                prefix.occurrences += occurrences
                updated_prefixes.append(prefix)
            for suffix_token, weight in graph[prefix_tokens].items():
                if created_prefix:
                    suffix, created_suffix = (prefix.suffixes.create(token=suffix_token, weight=weight), True)
                else:
                    suffix, created_suffix = prefix.suffixes.get_or_create(token=suffix_token, defaults={'weight': weight})
                if not created_suffix:
                    suffix.weight += weight
                    updated_suffixes.append(suffix)
        self.prefixes.bulk_update(updated_prefixes, ['occurrences'])
        Suffix.objects.bulk_update(updated_suffixes, ['weight'])
        print('')
        self.trained_on.add(source)


    def random_sequence(self):
        prefix_tokens = deque([''] * (self.n-1), maxlen=self.n-1)
        sequence = list(prefix_tokens)
        while True:
            prefix_text = ''.join(prefix_tokens)
            suffix = self.prefixes.get(tokens=prefix_text).random_suffix()
            prefix_tokens.append(suffix.token)
            sequence.append(suffix.token)
            if suffix.token == '':
                return sequence

    def random_text(self):
        return ''.join(self.random_sequence())

    def __str__(self):
        return self.name


class Prefix(models.Model):
    markov = models.ForeignKey(Markov, on_delete=models.CASCADE, related_name='prefixes')
    tokens = models.CharField(max_length=500)  # FIXME: Check that it's the right number of tokens
    occurrences = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['markov']
        unique_together = ['markov', 'tokens']

    def __str__(self):
        return self.tokens

    def random_suffix(self):
        threshhold = random.random() * self.occurrences
        upto = 0.0
        for suffix in self.suffixes.all():
            upto += suffix.weight
            if upto >= threshhold:
                return suffix


class Suffix(models.Model):
    prefix = models.ForeignKey(Prefix, on_delete=models.CASCADE, related_name='suffixes')
    token = models.CharField(max_length=500)  # FIXME: Check that it's just one token
    weight = models.PositiveIntegerField()

    class Meta:
        ordering = ['prefix', '-weight']
        unique_together = ['prefix', 'token']

    def __str__(self):
        return self.token
