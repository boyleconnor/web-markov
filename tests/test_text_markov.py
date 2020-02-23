from text_markov import TextMarkov
from unittest import TestCase


class TextMarkovTest(TestCase):
    def test_read_blank_text(self):
        new_ngram = TextMarkov(4)
        new_ngram.read_text('')
        self.assertIn(('', '', '', ''), new_ngram.get_ngrams('', '', ''))

    def test_read_text(self):
        markov = TextMarkov(3)
        markov.read_text('hello world')
        self.assertIn(('', '', 'hello'), markov.get_ngrams('', ''))
        self.assertIn(('', 'hello', ' '), markov.get_ngrams('', 'hello'))
        self.assertAlmostEqual(markov.get_ngrams('hello', ' ' )[('hello', ' ', 'world')], 1)
        self.assertIn((' ', 'world', ''), markov.get_ngrams(' ', 'world'))

        markov.read_text('hello world')
        markov.read_text('hello, world')
        self.assertIn(('', 'hello', ' '), markov.get_ngrams('', 'hello'))
        self.assertAlmostEqual(markov.get_ngrams('', 'hello')[('', 'hello', ', ')], 1 / 3)
