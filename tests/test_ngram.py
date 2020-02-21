from unittest import TestCase
from ngram_model import NGram


class NGramTest(TestCase):
    def test_initialize(self):
        ngram = NGram(3)

    def test_add_ngram(self):
        ngram = NGram(3)
        ngram.add_ngram('hello', 'there', 'sir')

    def test_add_wrong_length_ngram(self):
        ngram = NGram(3)
        with self.assertRaises(ValueError) as context:
            ngram.add_ngram('hello', 'world')
