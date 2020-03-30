from rest_framework import serializers
from MarkovApp.models import Source, SingleMarkov, MergedMarkov


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['name', 'source_file']


class SingleMarkovSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = SingleMarkov
        fields = ['source', 'ngram_size']


class MergedMarkovSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = MergedMarkov
        fields = ['source_one', 'source_two', 'ngram_size']
