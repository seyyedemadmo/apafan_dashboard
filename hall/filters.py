from rest_framework.filters import BaseFilterBackend
from guardian.shortcuts import get_objects_for_user


class HallListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_admin:
            return queryset.filter(company_id=request.user.company.id)
        return get_objects_for_user(request.user,
                                    f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")


class ProductionListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_admin:
            return queryset.filter(hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user,
                                    f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")


class GroupListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_admin:
            return queryset.filter(production__hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user, f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")


class DeviceListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_admin:
            return queryset.filter(group__production__hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user, f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")


class HeadListObjectPermissionFilterBackend(BaseFilterBackend):
    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        if request.user.is_admin:
            return queryset.filter(device_group__production__hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user, f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")
