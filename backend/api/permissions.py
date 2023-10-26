from rest_framework import permissions


class OnlyRead(permissions.BasePermission):
    """Доступ только для безопасных методов"""

    def has_permission(self, request, view):
        return request.method in permissions.SAFE_METHODS

    def has_object_permission(self, request, view, obj):
        return request.method in permissions.SAFE_METHODS


class Author(permissions.BasePermission):
    """Доступ только автору записи."""

    def has_permission(self, request, view):
        return request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        return obj.author == request.user
