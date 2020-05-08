from django.test import TestCase
from django.core.files import File
from .models import Source, Markov, Training


class DeterministicMarkovTests(TestCase):
    def test_read_text(self):
        markov = Markov.objects.create()
        markov.read_text('hello world')
        self.assertIn('hello', markov.graph)
        self.assertEqual(markov.graph['hello'], {' ': 1})

    # FIXME: Rigorously test that this actually trains on the file
    def test_train_on_source(self):
        with open('../sources/trump.txt', 'rb') as trump_file:
            mock_file = File(trump_file, name='trump.txt')
            trump_source = Source.objects.create(file=mock_file, name="Trump's Twitter")
            markov = Markov.objects.create(name="TrumpBot")
            Training.objects.create(markov=markov, source=trump_source)
            trump_source.file.delete()

    def test_random_sequence(self):
        markov = Markov.objects.create(n=5, tokenizer='\w+|\W+')
        markov.read_text('hello, world')
        sequence = markov.random_sequence()
        self.assertEqual(sequence, ['', '', '', '', 'hello', ', ', 'world', ''])


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
        ITERATIONS = 20000
        for i in range(ITERATIONS):
            random_text = markov.random_text()
            self.assertIn(random_text, {'hello world', 'hello friend'})
            if random_text == 'hello world':
                world_count += 1
            elif random_text == 'hello friend':
                friend_count += 1
        self.assertAlmostEqual(world_count / ITERATIONS, 2 / 3, 2)
        self.assertAlmostEqual(friend_count / ITERATIONS, 1 / 3, 2)
