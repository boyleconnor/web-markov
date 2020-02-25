from unittest import TestCase
from markov import Markov


class DeterministicTests(TestCase):
    def test_initialize(self):
        markov = Markov(3)

    def test_add_ngram(self):
        markov = Markov(3)
        markov.add_ngram('hello', 'there', 'sir')
        markov.add_ngram('hello', 'there', 'sir')
        markov.add_ngram('hello', 'there', 'man')
        markov.add_ngram('hello', 'mister', 'man')

    def test_add_wrong_length_ngram(self):
        markov = Markov(3)
        with self.assertRaises(ValueError) as context:
            markov.add_ngram('hello', 'world')

    def test_get_ngrams(self):
        markov = Markov(3)
        markov.add_ngram('hello', 'there', 'sir')
        markov.add_ngram('hello', 'there', 'sir')
        markov.add_ngram('hello', 'there', 'world')
        markov.add_ngram('hello', 'mister', 'Smith')
        markov.add_ngram('hello', 'mister', 'Boyle')

        hello_mister = markov.get_ngrams('hello', 'mister')
        hello_mister_boyle = ('hello', 'mister', 'Boyle')
        self.assertIn(hello_mister_boyle, hello_mister)
        self.assertAlmostEqual(hello_mister[hello_mister_boyle], 1 / 2)

        hello_there = markov.get_ngrams('hello', 'there')
        hello_there_sir = ('hello', 'there', 'sir')
        self.assertIn(hello_there_sir, hello_there)
        self.assertAlmostEqual(hello_there[hello_there_sir], 2 / 3)
        self.assertNotIn(hello_mister_boyle, hello_there)

    def test_get_suffixes(self):
        markov = Markov(2)
        markov.add_ngram('hello', 'world')
        markov.add_ngram('hello', 'world')
        markov.add_ngram('hello', 'Connor')

        self.assertIn('Connor', markov.get_suffixes('hello'))
        self.assertIn('world', markov.get_suffixes('hello'))
        self.assertAlmostEqual(markov.get_suffixes('hello')['Connor'], 1 / 3)

    def test_update(self):
        model_one = Markov(2)
        model_one.add_ngram('goodbye', 'friend')
        model_one.add_ngram('hello', 'world')

        model_two = Markov(2)
        model_two.add_ngram('hello', 'world')
        model_two.add_ngram('hello', 'Connor')

        model_two.update(model_one)

        self.assertAlmostEqual(model_two.get_suffixes('hello')['Connor'], 1 / 3)
        self.assertAlmostEqual(model_two.get_suffixes('hello')['world'], 2 / 3)
        self.assertAlmostEqual(model_two.get_suffixes('goodbye')['friend'], 1.0)
        self.assertAlmostEqual(model_one.get_suffixes('goodbye')['friend'], 1.0)
        self.assertAlmostEqual(model_one.get_suffixes('hello')['world'], 1.0)

    def test_blank_update(self):
        model_one = Markov(2)
        model_two = Markov(2)
        model_two.update(model_one)
        self.assertEqual(len(model_two.graph), 0)  # FIXME: Tests class internal (Markov.graph)

    def test_mismatched_update(self):
        model_one = Markov(2)
        model_two = Markov(3)

        with self.assertRaises(ValueError) as context:
            model_two.update(model_one)


class ProbabilisticTests(TestCase):  # TODO: Test Markov.random_suffix method
    def test_random_ngram(self):
        ITERATIONS = 10000

        markov = Markov(3)
        for i in range(9):
            markov.add_ngram('hello', 'there', 'world')
        markov.add_ngram('hello', 'there', 'sir')

        world_count = 0
        sir_count = 0
        for i in range(ITERATIONS):
            random_ngram = markov.random_ngram('hello', 'there')
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

    def test_random_suffix(self):
        ITERATIONS = 20000

        markov = Markov(2)
        markov.add_ngram('hello', 'world')
        for i in range(20):
            markov.add_ngram('goodbye', 'world')
        for i in range(5):
            markov.add_ngram('goodbye', 'Jessica')

        world_count = 0
        jessica_count = 0
        for i in range(ITERATIONS):
            random_suffix = markov.random_suffix('goodbye')
            if random_suffix == 'world':
                world_count += 1
            if random_suffix == 'Jessica':
                jessica_count += 1

        self.assertAlmostEqual(world_count / ITERATIONS, 4 / 5, 2)
        self.assertAlmostEqual(jessica_count / ITERATIONS, 1 / 5, 2)
