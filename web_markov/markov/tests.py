from django.test import TestCase
from django.core.files import File
from .models import Source, Markov


class DeterministicMarkovTests(TestCase):
    def test_read_text(self):
        markov = Markov.objects.create()
        markov.read_text('hello world')
        self.assertTrue(markov.prefixes.filter(tokens='').exists())
        start_of_text = markov.prefixes.get(tokens='')
        self.assertEqual(start_of_text.suffixes.get().token, 'hello')
        self.assertEqual(start_of_text.suffixes.get().weight, 1)
        markov.read_text('hello world')
        markov.read_text('hello friend')
        hello__prefix = markov.prefixes.get(tokens='hello ')
        self.assertEqual(hello__prefix.suffixes.count(), 2)
        self.assertEqual(hello__prefix.occurrences, 3)
        self.assertEqual(hello__prefix.suffixes.get(token='world').weight, 2)
        self.assertEqual(hello__prefix.suffixes.get(token='friend').weight, 1)

    def test_train_on_source(self):
        with open('../sources/trump.txt', 'rb') as trump_file:
            mock_file = File(trump_file, name='trump.txt')
            trump_source = Source.objects.create(source_file=mock_file, name="Trump's Twitter")
            markov = Markov.objects.create(name="TrumpBot")
            markov.train_on(trump_source)  # FIXME: This is still way too slow.
            self.assertIn(trump_source, markov.trained_on.all())
            print("Random Trump tweet:")
            print(markov.random_text())
            trump_source.source_file.delete()


class NonDeterministicMarkovTests(TestCase):
    '''These tests depend on random behavior. They run the functions in
    question through thousands of iterations, so the tests are unlikely to
    fail if the functions being tested have been implemented correctly.
    '''
    def test_random_text(self):
        markov = Markov.objects.create()
        markov.read_text('hello world')
        markov.read_text('hello world')
        markov.read_text('hello friend')

        world_count = 0
        friend_count = 0
        ITERATIONS = 100
        for i in range(ITERATIONS):
            random_text = markov.random_text()
            self.assertIn(random_text, {'hello world', 'hello friend'})
            if random_text == 'hello world':
                world_count += 1
            elif random_text == 'hello friend':
                friend_count += 1
        self.assertAlmostEqual(world_count / ITERATIONS, 2 / 3, 1)
        self.assertAlmostEqual(friend_count / ITERATIONS, 1 / 3, 1)
