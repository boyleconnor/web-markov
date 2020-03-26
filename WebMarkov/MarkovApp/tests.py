from django.test import TestCase
from MarkovApp.models import Source, SingleMarkov, MergedMarkov
from django.core.files import File

# Create your tests here.

class SingleMarkovTest(TestCase):
    def test_initializer(self):
        with open('MarkovMerge/sources/hamlet.txt', 'rb') as hamlet_file:
            mock_file = File(hamlet_file, name='hamlet.txt')
            hamlet_source = Source.objects.create(source_file=mock_file, name="Shakespeare's Hamlet")
            hamlet_markov = SingleMarkov.objects.create(source=hamlet_source)
            hamlet_source.source_file.delete()

    def test_generate_text(self):
        with open('MarkovMerge/sources/trump.txt', 'rb') as trump_file:
            mock_file = File(trump_file, name='trump.txt')
            trump_source = Source.objects.create(source_file=mock_file, name="Trump's Twitter")
            trump_markov = SingleMarkov.objects.create(source=trump_source)
            random_text = trump_markov.markov_model.random_text()
            self.assertGreater(len(random_text), 1)
            trump_source.source_file.delete()

    def test_get_from_db(self):
        with open('MarkovMerge/sources/frankenstein.txt', 'rb') as frankenstein_file:
            mock_file = File(frankenstein_file, name='frankenstein.txt')
            Source.objects.create(source_file=mock_file, name='Frankenstein')
            frankenstein_source = Source.objects.get()
            SingleMarkov.objects.create(source=frankenstein_source)
            frankenstein_markov = SingleMarkov.objects.get()
            self.assertEqual(frankenstein_markov.pk, 1)
            frankenstein_source.source_file.delete()


class MergedMarkovTests(TestCase):
    def test_initializer(self):
        hamlet_file = open('MarkovMerge/sources/hamlet.txt', 'rb')
        mock_hamlet = File(hamlet_file, name='hamlet.txt')
        hamlet_source = Source.objects.create(source_file=mock_hamlet, name='Hamlet')

        trump_file  = open('MarkovMerge/sources/trump.txt', 'rb')
        mock_trump = File(trump_file, name='trump.txt')
        trump_source = Source.objects.create(source_file=mock_trump, name='Trump tweets')

        merged = MergedMarkov.objects.create(source_one=trump_source, source_two=hamlet_source)
        hamlet_source.source_file.delete()
        trump_source.source_file.delete()

    def test_generate_sequence(self):
        hamlet_file = open('MarkovMerge/sources/hamlet.txt', 'rb')
        mock_hamlet = File(hamlet_file, name='hamlet.txt')
        hamlet_source = Source.objects.create(source_file=mock_hamlet, name='Hamlet')

        trump_file  = open('MarkovMerge/sources/trump.txt', 'rb')
        mock_trump = File(trump_file, name='trump.txt')
        trump_source = Source.objects.create(source_file=mock_trump, name='Trump tweets')

        merged = MergedMarkov.objects.create(source_one=trump_source, source_two=hamlet_source)
        random_text = merged.markov_model.random_sequence()
        merged.source_one.source_file.delete()
        merged.source_two.source_file.delete()
