from rest_framework.permissions import BasePermission, SAFE_METHODS


class UserCanCreate(BasePermission):
    def has_permission(self, request, view):
        if request.method == 'POST':
            return request.user.is_authenticated
        return False

    def has_object_permission(self, request, view, object):
        return False


class OwnerCanEdit(BasePermission):
    message = 'Current user is not the owner of the requested object'

    def has_permission(self, request, view):
        return request.method in ('POST', 'DELETE')

    def has_object_permission(self, request, view, object):
        return request.user == object.owner


class ReadOnly(BasePermission):
    def has_permission(self, request, view):
        return request.method in SAFE_METHODS

    def has_object_permission(self, request, view, object):
        return self.has_permission(request, view)
