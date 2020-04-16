from rest_framework import serializers
from MarkovApp.models import Source, Markov


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['url', 'id', 'name', 'source_file']


class MarkovSerializer(serializers.HyperlinkedModelSerializer):
    # trained_on = SourceSerializer(read_only=True)

    class Meta:
        model = Markov
        fields = ['url', 'id', 'name', 'n', 'tokenizer', 'trained_on']
