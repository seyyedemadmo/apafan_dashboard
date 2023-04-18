from guardian.shortcuts import get_objects_for_user
from rest_framework.filters import BaseFilterBackend


class HeadParametersFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        elif request.user.is_admin:
            return queryset.filter(head_device_group__production__hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user,
                                    f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")


class DeviceParameterFilterBackend(BaseFilterBackend):

    def filter_queryset(self, request, queryset, view):
        if request.user.is_superuser:
            return queryset
        elif request.user.is_admin:
            return queryset.filter(device__group__production__hall__company_id=request.user.company.id)
        return get_objects_for_user(request.user,
                                    f"{queryset.model._meta.app_label}.view_{queryset.model._meta.model_name}")
