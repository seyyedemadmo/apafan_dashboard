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
        return self.has_object_permission(request, view, view.get_object())

    def has_object_permission(self, request, view, obj):
        return request.user.has_perm(
            f"{view.queryset.model._meta.app_label}.view_{view.queryset.model._meta.model_name}", obj)
