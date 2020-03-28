from io import TextIOWrapper
from django.db.models import Model, FileField, PositiveSmallIntegerField, CharField, ForeignKey, CASCADE
from django.urls import reverse
from picklefield.fields import PickledObjectField
from MarkovMerge.models.text_markov import TextMarkov
from MarkovMerge.models.text_merger import TextMerger

DEFAULT_NGRAM_SIZE = 5


class Source(Model):
    name = CharField(max_length=100, blank=False, unique=True)
    source_file = FileField(upload_to='sources/')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('source_detail', kwargs={'pk': self.pk})


class SingleMarkov(Model):
    source = ForeignKey(Source, on_delete=CASCADE)
    ngram_size = PositiveSmallIntegerField(default=DEFAULT_NGRAM_SIZE)
    markov_model = PickledObjectField()

    class Meta:
        unique_together = ['source', 'ngram_size']

    def get_absolute_url(self):
        return reverse('singlemarkov_detail', kwargs={'pk': self.pk})

    def __str__(self):
        return '"%s" (n = %d)' % (self.source.name, self.ngram_size)

    def save(self, *args, **kwargs):
        '''Enforces the following: .markov_model is a TextMarkov based off the
        contents of .source_file.
        '''
        if self.markov_model is None:
            self.markov_model = TextMarkov(self.ngram_size)
            wrapper = TextIOWrapper(self.source.source_file)  # FIXME: This seems hacky
            for line in wrapper:
                self.markov_model.read_text(line)
        return super().save(*args, **kwargs)


class MergedMarkov(Model):
    ngram_size = PositiveSmallIntegerField(default=DEFAULT_NGRAM_SIZE)
    source_one = ForeignKey(Source, on_delete=CASCADE, related_name='merged_one')
    source_two = ForeignKey(Source, on_delete=CASCADE, related_name='merged_two')
    markov_model = PickledObjectField()

    class Meta:
        unique_together = ['source_one', 'source_two', 'ngram_size']

    def get_absolute_url(self):
        return reverse('mergedmarkov_detail', kwargs={'pk': self.pk})

    def save(self, *args, **kwargs):
        '''Enforces the following: .markov_model is a TextMerger based off
        .source_one and .source_two.
        '''
        if self.markov_model is None:
            self.markov_model = TextMerger(self.ngram_size,
                    TextIOWrapper(self.source_one.source_file),
                    TextIOWrapper(self.source_two.source_file))  # FIXME: The TextIOWrapper's seem hacky
        return super().save(*args, **kwargs)
