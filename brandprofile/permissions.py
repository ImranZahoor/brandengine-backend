from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsAuthenticatedOrReadOnlyForList(BasePermission):
    """
    Custom permission to only allow authenticated users to perform non-read-only actions.
    """

    def has_permission(self, request, view):
        # Allow anyone to list (read-only)
        if view.action == "list":
            return True
        # Require authentication for other actions
        return request.user and request.user.is_authenticated
