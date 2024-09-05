from rest_framework.permissions import BasePermission


class IsOwner(BasePermission):
    """Возвращает признак владельца привычки."""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
