from rest_framework import serializers
from MarkovApp.models import Source, SingleMarkov, MergedMarkov


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['url', 'name', 'source_file']


class SingleMarkovSerializer(serializers.HyperlinkedModelSerializer):
    source = SourceSerializer(read_only=True)

    class Meta:
        model = SingleMarkov
        fields = ['url', 'source', 'ngram_size']


class MergedMarkovSerializer(serializers.HyperlinkedModelSerializer):
    source_one = SourceSerializer(read_only=True)
    source_two = SourceSerializer(read_only=True)

    class Meta:
        model = MergedMarkov
        fields = ['url', 'source_one', 'source_two', 'ngram_size']
