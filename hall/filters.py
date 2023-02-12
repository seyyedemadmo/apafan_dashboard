from rest_framework.filters import BaseFilterBackend
from guardian.shortcuts import get_objects_for_user


class ListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_admin:
            return queryset
        return get_objects_for_user(request.user, f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")
