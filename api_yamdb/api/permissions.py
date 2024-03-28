from rest_framework.permissions import (
    BasePermission,
    SAFE_METHODS,
)


class IsAdminOrSuperuserOrReadOnly(BasePermission):
    """Allow non-safe methods for admin and superuser."""

    def has_permission(self, request, view):
        return (
            request.method in SAFE_METHODS
            or (
                request.user.is_authenticated
                and request.user.is_admin
            )
        )


class IsAdminOrSuperuser(BasePermission):
    """Allow methods for admin and superuser."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )


class IsAuthorOrModeratorOrAdminOrSuperuser(BasePermission):
    """Allow non-safe methods for author, moderator, admin, superuser."""

    def has_object_permission(self, request, view, obj):
        return (
            request.method in SAFE_METHODS
            or request.user.is_authenticated
            and (request.user.is_admin
                 or request.user.is_moderator
                 or request.user == obj.author)
        )
