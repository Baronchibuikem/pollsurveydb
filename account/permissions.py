from rest_framework import permissions


# class IsOwner(permissions.BasePermission):
#     """
#     Custom of class IsOwnerOrReadOnly(permissions.BasePermission)
#     That an APIexception is raised instead
#     We do not want a ReadOnly
#     """

#     def has_object_permission(self, request, view, obj):

#         # First check if authentication is TrueD
#   return obj.owner == request.user

class IsOwnerOrReadonly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.owner == request.user
