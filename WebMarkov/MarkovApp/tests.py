from django.test import TestCase
from MarkovApp.models import SingleMarkov, MergedMarkov
from django.core.files import File

# Create your tests here.

class SingleMarkovTest(TestCase):
    def test_initializer(self):
        with open('MarkovMerge/sources/hamlet.txt', 'rb') as hamlet:
            hamlet_file = File(hamlet, name='hamlet.txt')
            single_markov = SingleMarkov.objects.create(source_file=hamlet_file)
        single_markov.source_file.delete()
        single_markov.delete()

    def test_generate_text(self):
        with open('MarkovMerge/sources/trump.txt', 'rb') as trump:
            trump_file = File(trump, name='trump.txt')
            markov_one = SingleMarkov.objects.create(source_file=trump_file)
        random_text = markov_one.markov_model.random_text()
        self.assertGreater(len(random_text), 1)
        markov_one.source_file.delete()
        markov_one.delete()

    def test_get_from_db(self):
        with open('MarkovMerge/sources/frankenstein.txt', 'rb') as frankenstein:
            frankenstein_file = File(frankenstein, name='frankenstein.txt')
            SingleMarkov.objects.create(source_file=frankenstein_file)

        frankenstein_markov = SingleMarkov.objects.get()
        self.assertEqual(frankenstein_markov.pk, 1)
        frankenstein_markov.source_file.delete()
        frankenstein_markov.delete()
