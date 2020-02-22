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

    def test_random_ngram(self):
        ITERATIONS = 10000

        ngram = NGram(3)
        for i in range(9):
            ngram.add_ngram('hello', 'there', 'world')
        ngram.add_ngram('hello', 'there', 'sir')

        world_count = 0
        sir_count = 0
        for i in range(ITERATIONS):
            random_ngram = ngram.random_ngram('hello', 'there')
            if random_ngram == ('hello', 'there', 'world'):
                world_count += 1
            if random_ngram == ('hello', 'there', 'sir'):
                sir_count += 1

        world_share = world_count / ITERATIONS
        sir_share = sir_count / ITERATIONS

        self.assertGreater(world_share, 0.85)
        self.assertLess(world_share, 0.95)
        self.assertGreater(sir_share, 0.05)
        self.assertLess(sir_share, 0.15)

    def test_read_text(self):
        ngram = NGram(3)
        ngram.read_text('hello world')
        self.assertIn(('', '', 'hello'), ngram.get_ngrams('', ''))
        self.assertIn(('', 'hello', ' '), ngram.get_ngrams('', 'hello'))
        self.assertAlmostEqual(ngram.get_ngrams('hello', ' ' )[('hello', ' ', 'world')], 1)
        self.assertIn((' ', 'world', ''), ngram.get_ngrams(' ', 'world'))

        ngram.read_text('hello world')
        ngram.read_text('hello, world')
        self.assertIn(('', 'hello', ' '), ngram.get_ngrams('', 'hello'))
        self.assertAlmostEqual(ngram.get_ngrams('', 'hello')[('', 'hello', ', ')], 1 / 3)

    def test_read_blank_text(self):
        new_ngram = NGram(4)
        new_ngram.read_text('')
        self.assertIn(('', '', '', ''), new_ngram.get_ngrams('', '', ''))
