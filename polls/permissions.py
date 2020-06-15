from django.db.models import Q

from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission


from .models import Vote



class IsPollChoiceOwner(BasePermission):
    """
    Custom of class IsOwnerOrReadOnly(permissions.BasePermission)
    That an APIexception is raised instead
    We do not want a ReadOnly
    """

    def has_object_permission(self, request, view, obj):
        # Instance is the user
        return obj.poll.poll_creator.id == request.user.id


class IsPollOwner(BasePermission):
    """
    Custom of class IsOwnerOrReadOnly(permissions.BasePermission)
    That an APIexception is raised instead
    We do not want a ReadOnly
    """

    def has_object_permission(self, request, view, obj):
        # Instance is the user
        return obj.poll_creator.id == request.user.id
