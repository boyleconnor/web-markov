from django.forms import ModelForm
from MarkovApp.models import Source, SingleMarkov


class SourceForm(ModelForm):
    class Meta:
        model = Source
        fields = ['source_file', 'name']


class SingleMarkovForm(ModelForm):
    class Meta:
        model = SingleMarkov
        fields = ['source', 'ngram_size']
