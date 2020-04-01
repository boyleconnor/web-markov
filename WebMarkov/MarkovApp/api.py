from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import action
from MarkovApp.models import Source, SingleMarkov, MergedMarkov
from MarkovApp.serializers import SourceSerializer, SingleMarkovSerializer, \
        MergedMarkovSerializer


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SingleMarkovViewSet(ModelViewSet):
    queryset = SingleMarkov.objects.all()
    serializer_class = SingleMarkovSerializer

    @action(detail=True)
    def random_sequence(self, request, pk=None):
        markov_model = self.get_object().markov_model
        prefix_length = markov_model.n - 1
        prefix = ('',) * prefix_length
        return Response({
            'sequence': markov_model.random_sequence(*prefix)
        })


class MergedMarkovViewSet(ModelViewSet):
    queryset = MergedMarkov.objects.all()
    serializer_class = MergedMarkovSerializer

    @action(detail=True)
    def random_sequence(self, request, pk=None):
        text_merger = self.get_object().markov_model
        sequence = text_merger.random_sequence()
        biases = text_merger.get_biases(*sequence)
        return Response({
            'sequence': sequence,
            'biases': biases
        })


api_router = DefaultRouter()
api_router.register('source', SourceViewSet)
api_router.register('single_markov', SingleMarkovViewSet)
api_router.register('merged_markov', MergedMarkovViewSet)
