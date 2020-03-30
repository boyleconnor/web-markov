from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.decorators import action
from MarkovApp.models import Source, SingleMarkov, MergedMarkov
from MarkovApp.serializers import SourceSerializer, SingleMarkovSerializer, MergedMarkovSerializer


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class SingleMarkovViewSet(ModelViewSet):
    queryset = SingleMarkov.objects.all()
    serializer_class = SingleMarkovSerializer


class MergedMarkovViewSet(ModelViewSet):
    queryset = MergedMarkov.objects.all()
    serializer_class = MergedMarkovSerializer


api_router = DefaultRouter()
api_router.register('source', SourceViewSet)
api_router.register('single_markov', SingleMarkovViewSet)
api_router.register('merged_markov', MergedMarkovViewSet)
