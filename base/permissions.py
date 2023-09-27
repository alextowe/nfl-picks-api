from rest_framework import permissions
from base.models import User


class IsOwner(permissions.BasePermission):
    """
    Grants the owner permission to edit objects.
    """
 
    def has_object_permission(self, request, view, obj):
        """
        Checks if user is owner of object.
        """
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user
        
        return obj.owner == request.user

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Grants the owner permission to edit objects and grants non-owners read only access.  
    """

    def has_object_permission(self, request, view, obj):
        """
        Checks if user is owner of object. Returns 'True' for 'SAFE_METHODS' (GET, HEAD and OPTIONS).
        """

        if request.method in permissions.SAFE_METHODS:
            return True
        
        if hasattr(obj, 'owner'):
            return obj.owner == request.user

        return obj == request.user