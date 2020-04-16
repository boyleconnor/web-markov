from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import action
from MarkovApp.models import Source, Markov
from MarkovApp.serializers import SourceSerializer, MarkovSerializer


class SourceViewSet(ModelViewSet):
    queryset = Source.objects.all()
    serializer_class = SourceSerializer


class MarkovViewSet(ModelViewSet):
    queryset = Markov.objects.all()
    serializer_class = MarkovSerializer

    @action(detail=True)
    def random_text(self, request, pk=None):
        return Response({
            'text': self.get_object().random_text()
        })

    @action(detail=True, methods=['post'])
    def train_on(self, request, pk=None):
        source = Source.objects.get(id=request.data['source'])
        self.get_object().train_on(source)


api_router = DefaultRouter()
api_router.register('source', SourceViewSet)
api_router.register('markov', MarkovViewSet)
