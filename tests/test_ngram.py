from unittest import TestCase
from ngram_model import NGram


class NGramTest(TestCase):
    def test_initialize(self):
        ngram = NGram(3)

    def test_add_ngram(self):
        ngram = NGram(3)
        ngram.add_ngram('hello', 'there', 'sir')
        ngram.add_ngram('hello', 'there', 'sir')
        ngram.add_ngram('hello', 'there', 'man')
        ngram.add_ngram('hello', 'mister', 'man')

    def test_add_wrong_length_ngram(self):
        ngram = NGram(3)
        with self.assertRaises(ValueError) as context:
            ngram.add_ngram('hello', 'world')

    def test_get_ngrams(self):
        ngram = NGram(3)
        ngram.add_ngram('hello', 'there', 'sir')
        ngram.add_ngram('hello', 'there', 'sir')
        ngram.add_ngram('hello', 'there', 'world')
        ngram.add_ngram('hello', 'mister', 'Smith')
        ngram.add_ngram('hello', 'mister', 'Boyle')

        hello_mister = ngram.get_ngrams('hello', 'mister')
        hello_mister_boyle = ('hello', 'mister', 'Boyle')
        self.assertIn(hello_mister_boyle, hello_mister)
        self.assertAlmostEqual(hello_mister[hello_mister_boyle], 1 / 2)

        hello_there = ngram.get_ngrams('hello', 'there')
        hello_there_sir = ('hello', 'there', 'sir')
        self.assertIn(hello_there_sir, hello_there)
        self.assertAlmostEqual(hello_there[hello_there_sir], 2 / 3)
        self.assertNotIn(hello_mister_boyle, hello_there)
