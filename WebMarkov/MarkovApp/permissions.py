from rest_framework.permissions import BasePermission, SAFE_METHODS
from django.shortcuts import get_object_or_404
from .models import Markov


class UserCanCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, object):
        return False


class OwnerCanDelete(BasePermission):
    message = 'Current user is not the owner of the requested object'

    def has_permission(self, request, view):
        return request.method == 'DELETE'

    def has_object_permission(self, request, view, object):
        return request.user == object.owner


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)


class MarkovOwnerCanTrain(BasePermission):
    message = 'Current user is not the owner of the requested markov model'

    def has_permission(self, request, view):
        if request.method == 'POST':
            serializer = view.get_serializer(data=request.data)
            if serializer.is_valid():
                markov_pk = serializer.data['markov']
                markov = get_object_or_404(Markov, pk=markov_pk)
                return markov.owner == request.user
            return True  # Invalid serializer can't be saved, so we're safe!

        # FIXME: Allow models to be untrained (i.e. with DELETE method)
        elif request.method == 'GET':  
            return True

        return False

    def has_object_permission(self, request, view, object):
        # FIXME: In the future, "trainings" should be deletable
        return False
