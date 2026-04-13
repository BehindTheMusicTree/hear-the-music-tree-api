from rest_framework.exceptions import NotAuthenticated
from rest_framework.permissions import BasePermission


class IsAuthenticatedReturn401(BasePermission):
    """
    Permission that returns 401 (via NotAuthenticated) when the user is not
    authenticated, instead of DRF's default 403 (PermissionDenied).
    """

    def has_permission(self, request, view):
        if request.user and request.user.is_authenticated:
            return True
        raise NotAuthenticated(detail={"detail": "Authentication required", "code": "authentication_required"})
