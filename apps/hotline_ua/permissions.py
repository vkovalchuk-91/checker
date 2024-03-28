from rest_framework.permissions import BasePermission


class CustomPermission(BasePermission):

    def has_permission(self, request, view):
        user = request.user
        return user.is_superuser or (user.is_authenticated and user.is_active)
