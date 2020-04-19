import random
import re
from collections import deque
from io import TextIOWrapper
from django.db import models
from django.conf import settings
from .client import Client



# Connect to the MarkovMerge server
host_name, port = settings.MARKOV_MERGE_SERVER_ADDRESS
client = Client(host_name, port)


class Source(models.Model):
    name = models.CharField(max_length=100, blank=False, unique=True)
    source_file = models.FileField(upload_to='sources/')
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
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
    trained_on = models.ManyToManyField(Source, blank=True)
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )
    saved_to_markov_merge = models.BooleanField(default=False)

    def train_on(self, source):
        if self.trained_on.filter(pk=source.pk).exists():
            raise ValueError("Model has already been trained on source: %s" % (source,))
        client.train_model(str(self.pk), [line.decode() for line in source.source_file.readlines()])
        self.trained_on.add(source)

    def random_text(self):
        return client.random_text(str(self.pk))['result']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        # Add model on MarkovMerge server
        result = super().save(*args, **kwargs)
        if not self.saved_to_markov_merge:
            client.add_model(str(self.pk), self.n, self.tokenizer)
            self.saved_to_markov_merge = True
            result = super().save()
        return result
