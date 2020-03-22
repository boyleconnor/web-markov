from django.forms import ModelForm
from MarkovApp.models import SingleMarkov


class SingleMarkovForm(ModelForm):
    class Meta:
        model = SingleMarkov
        fields = ['source_file', 'ngram_size']
