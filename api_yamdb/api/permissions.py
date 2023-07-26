from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Доступ только владельцу записи."""
    def has_permission(self, request, view):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated)

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or request.user.is_authenticated and obj.author == request.user
                or request.user.is_moderator
                or request.user.is_admin)


class Moderator(permissions.BasePermission):
    """Доступ только модератор."""

    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_moderator

    def has_object_permission(self, request, view, obj):
        return request.user.is_moderator


class IsAdmin(permissions.BasePermission):
    """Доступ только администратор."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.is_admin
        )

    def has_object_permission(self, request, view, obj):
        return request.user.is_admin


class OnlyRead(permissions.BasePermission):
    """Доступ только для безопасных методов"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS
