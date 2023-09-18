from rest_framework import permissions

class IsOwner(permissions.BasePermission):
    """
    Custom permission
    """

    def has_object_permission(self, request, view, obj):
        # Write permissions are only allowed to the owner.
        return obj == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner.
        return obj == request.user