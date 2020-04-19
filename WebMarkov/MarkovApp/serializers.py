from django.contrib.auth import get_user_model
from rest_framework import serializers
from MarkovApp.models import Source, Markov


User = get_user_model()


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['url', 'id', 'username', 'source_set', 'markov_set']


class BasicUserSerializer(serializers.HyperlinkedModelSerializer):
    '''Serializer with basic user info, for nesting in other serializers.
    '''
    class Meta:
        model = User
        fields = ['url', 'username']


class SourceSerializer(serializers.HyperlinkedModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Source
        fields = ['url', 'id', 'name', 'source_file', 'owner']
        read_only_fields = ['owner']


class MarkovSerializer(serializers.HyperlinkedModelSerializer):
    owner = BasicUserSerializer(read_only=True)

    class Meta:
        model = Markov
        fields = ['url', 'id', 'name', 'n', 'tokenizer', 'trained_on', 'owner']
        read_only_fields = ['trained_on', 'owner']
