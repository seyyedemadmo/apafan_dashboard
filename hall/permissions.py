from rest_framework.permissions import BasePermission


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        try:
            if request.user.is_superuser:
                return True
            return False
        except:
            return False

class CustomObjectPermission(BasePermission):
    def has_permission(self, request, view):
        pass
    def has_object_permission(self, request, view, obj):
