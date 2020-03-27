from django.forms import ModelForm
from MarkovApp.models import Source, SingleMarkov, MergedMarkov


class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ['source_file', 'name']


class SingleMarkovForm(ModelForm):
    class Meta:
        model = SingleMarkov
        fields = ['source', 'ngram_size']


class MergedMarkovForm(ModelForm):
    class Meta:
        model = MergedMarkov
        fields = ['source_one', 'source_two', 'ngram_size']
