from rest_framework.permissions import DjangoObjectPermissions
from rest_framework.permissions import DjangoModelPermissions


class CustomDjangoObjectPermissions(DjangoObjectPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_object_permission(self, request, view, obj):
        if not request.user.is_anonymous and request.user.is_admin:
            return True
        else:
            return super(CustomDjangoObjectPermissions, self).has_object_permission(request, view, obj)

    def has_permission(self, request, view):
        if not request.user.is_anonymous and request.user.is_admin:
            return True
        return super(CustomDjangoObjectPermissions, self).has_permission(request, view)


class CustomDjangoModelPermissions(DjangoModelPermissions):
    perms_map = {
        'GET': [],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['%(app_label)s.add_%(model_name)s'],
        'PUT': ['%(app_label)s.change_%(model_name)s'],
        'PATCH': ['%(app_label)s.change_%(model_name)s'],
        'DELETE': ['%(app_label)s.delete_%(model_name)s'],
    }

    def has_permission(self, request, view):
        if request.user.is_admin:
            return True
        else:
            return super(CustomDjangoModelPermissions, self).has_permission(request, view)
