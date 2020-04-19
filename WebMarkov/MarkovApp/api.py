from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.routers import DefaultRouter
from rest_framework.response import Response
from rest_framework.decorators import action
from MarkovApp.models import Source, Markov
from MarkovApp.permissions import ReadOnly, OwnerCanEdit, UserCanCreate
from MarkovApp.serializers import SourceSerializer, MarkovSerializer, UserSerializer, RandomTextSerializer


User = get_user_model()


class UserViewSet(ModelViewSet):
    permission_classes = [ReadOnly]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class SourceViewSet(ModelViewSet):
    permission_classes = [OwnerCanEdit | ReadOnly | UserCanCreate]
    queryset = Source.objects.all()
    serializer_class = SourceSerializer

    # Assign owner to source
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class MarkovViewSet(ModelViewSet):
    permission_classes = [OwnerCanEdit | ReadOnly | UserCanCreate]
    queryset = Markov.objects.all()

    # Assign owner to markov
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True)
    def random_text(self, request, pk=None):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def train_on(self, request, pk=None):
        source = Source.objects.get(id=request.data['source'])
        self.get_object().train_on(source)

    def get_serializer_class(self):
        if self.action == 'random_text':
            return RandomTextSerializer
        else:
            return MarkovSerializer


api_router = DefaultRouter()
api_router.register('user', UserViewSet)
api_router.register('source', SourceViewSet)
api_router.register('markov', MarkovViewSet)
