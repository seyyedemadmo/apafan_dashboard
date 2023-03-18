from rest_framework.permissions import BasePermission


class IsAdminOrSuperUser(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        elif request.user.is_admin or request.user.is_superuser:
            return True
        return False
