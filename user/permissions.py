from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework.permissions import BasePermission


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        if request.user.is_anonymous:
            return False
        if request.user.is_admin or request.user.is_superuser:
            return True
        return False


class IsSelf(BasePermission):
    def has_permission(self, request, view):
        user = get_object_or_404(get_user_model(), username=view.kwargs['username'])
        if request.user == user:
            return True
        return False
