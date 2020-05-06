from django.contrib.auth import get_user_model
from rest_framework import serializers
from MarkovApp.models import Source, Markov, Training


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


class BasicSourceSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Source
        fields = ['url', 'id', 'name']


class MarkovTrainingSerializer(serializers.HyperlinkedModelSerializer):
    '''Serializes a training for a given (known) markov model.
    '''
    source = BasicSourceSerializer(read_only=True)

    class Meta:
        model = Training
        fields = ['url', 'source']


class MarkovSerializer(serializers.HyperlinkedModelSerializer):
    owner = BasicUserSerializer(read_only=True)
    random_text_url = serializers.HyperlinkedIdentityField(view_name='markov-random-text')
    trained_on = MarkovTrainingSerializer(read_only=True, many=True)

    class Meta:
        model = Markov
        fields = ['url', 'id', 'name', 'n', 'tokenizer', 'trained_on', 'owner', 'random_text_url', 'get_tokenizer_display']
        read_only_fields = ['trained_on', 'owner']


class RandomTextSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Markov
        fields = ['url', 'id', 'random_text']


class TrainingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Training
        fields = ['id', 'markov', 'source']
