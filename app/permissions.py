from rest_framework import permissions
from .models import Profile

class IsOwnerOrReadOnly(permissions.BasePermission):
    """
    Safe methods allowed to anyone. Unsafe methods require object owner (or staff).
    Works with objects that have `owner` or `user` attributes.
    """

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        owner = getattr(obj, "owner", None)
        if owner and getattr(owner, "user", None) == request.user:
            return True

        # For Profile objects, owner is obj.user
        if isinstance(obj, Profile) and obj.user == request.user:
            return True

        return bool(request.user and request.user.is_staff)


class IsHunarmand(permissions.BasePermission):
    """Allow only users with profile.role == 'hunarmand'"""

    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == "hunarmand")


class IsCollector(permissions.BasePermission):
    """Allow only collectors"""

    def has_permission(self, request, view):
        profile = getattr(request.user, "profile", None)
        return bool(profile and profile.role == "collector")