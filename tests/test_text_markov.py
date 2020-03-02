from unittest import TestCase
from models.text_markov import TextMarkov


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

    def test_random_text(self):
        ITERATIONS = 1000

        markov = TextMarkov(3)
        markov.read_text('hello world')
        self.assertEqual(markov.random_text(), 'hello world')

        markov.read_text('hello friend')
        random_texts = [markov.random_text() for i in range(ITERATIONS)]
        self.assertIn('hello friend', random_texts)
        self.assertIn('hello world', random_texts)
