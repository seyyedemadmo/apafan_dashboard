import datetime

from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.exceptions import ValidationError

from guardian.shortcuts import assign_perm

from Apafan_dashboard.authoraization import CustomAuthentication
from Apafan_dashboard.permissions import CustomDjangoObjectPermissions
from Apafan_dashboard.serializers import GlobalSerializer
from device.models import HeadData

from hall.apis.serializers import CompanySerializer, HallSerializer, ProductionSerializer, GroupSerializer, \
    DeviceSerializer, HeadSerializer, CompanyDetailSerializer, DeviceDetailSerialzier, DeviceDataSerializer
from hall.filters import *
from hall.permissions import IsSuperUser, CustomObjectPermission
from hall.models import Company, Hall, Production, Squad, Device, Head
from hall.utils.get_non_send_data import get_count_non_send


class CompanyViewSet(ModelViewSet):
    """ crud api for Company permission is super user only"""
    permission_classes = [IsSuperUser]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer

    @action(methods=["GET"], detail=True, permission_classes=[CustomDjangoObjectPermissions], )
    def list_halls(self, request, pk):
        hall_set = get_object_or_404(Company, id=pk).hall_set.all()
        available = get_objects_for_user(request.user,
                                         'hall.view_hall') if not request.user.is_admin else hall_set.filter(
            company_id=request.user.company.id)
        queryset = available & hall_set
        data = [HallSerializer(model).data for model in queryset]
        return Response(data=data, status=status.HTTP_200_OK)


class HallViewSet(ModelViewSet):
    """برای ساخت سالن های کارحانه ها این تنها برای کسانی که دسترسی ان را دارند فعال هست"""
    authentication_classes = [CustomAuthentication]
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [HallListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name']
    queryset = Hall.objects.all()
    serializer_class = HallSerializer

    def create(self, request, *args, **kwargs):
        res = super(HallViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_hall', request.user, get_object_or_404(Hall, id=res.data['id']))
        assign_perm('hall.change_hall', request.user, get_object_or_404(Hall, id=res.data['id']))
        return res

    @action(methods=["GET"], detail=True)
    def list_product(self, request, pk):
        hall_set = get_object_or_404(Hall, id=pk).production_set.all()
        available = get_objects_for_user(request.user,
                                         'hall.view_production') if not request.user.is_admin else hall_set
        queryset = available & hall_set
        data = ProductionSerializer(queryset, many=True)
        return Response(data=data, status=status.HTTP_200_OK)


class ProductionView(ModelViewSet):
    """برای ساخت و نمایش داده های خط تولید مورد استفاده قرار مگیرد این مجموعه نیز دارای دسترسی هستند"""
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [ProductionListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name']
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer

    def create(self, request, *args, **kwargs):
        res = super(ProductionView, self).create(request, *args, **kwargs)
        assign_perm('hall.view_production', request.user, get_object_or_404(Production, id=res.data['id']))
        assign_perm('hall.change_production', request.user, get_object_or_404(Production, id=res.data['id']))
        return res


class GroupViewSet(ModelViewSet):
    """برای نمایش داده های گروه ها و دارای دسترسی خاص خود"""
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [GroupListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name']
    queryset = Squad.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        res = super(GroupViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_squad', request.user, get_object_or_404(Squad, id=res.data['id']))
        assign_perm('hall.change_squad', request.user, get_object_or_404(Squad, id=res.data['id']))
        return res


class DeviceViewSet(ModelViewSet):
    """
    برای اسجاد دستگاه این مجموعه برای ورژن اول مورد نیاز هست و دارای دسترسی هست (در فاز اول تنها نیازی به پیاده سازی دسترسی ان نیست)
    """
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [DeviceListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name', 'code']
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer
    lookup_field = "pk"

    def create(self, request, *args, **kwargs):
        res = super(DeviceViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_device', request.user, get_object_or_404(Device, id=res.data['id']))
        assign_perm('hall.change_device', request.user, get_object_or_404(Device, id=res.data['id']))
        return res

    @action(methods=['GET'], detail=True)
    def get_parameter(self, request, pk):
        device = get_object_or_404(Device, id=pk)
        parameter_set = get_objects_for_user(self.request.user, "")

    @swagger_auto_schema(
        responses={200: openapi.Response('OK', DeviceDetailSerialzier)})
    @action(methods=["GET"], detail=False)
    def get_detail(self, request):
        try:
            all_device = len(self.get_queryset())
            active_device = len(self.get_queryset().filter(is_connected=True))
            deactivate_device = all_device - active_device
            non_send_data = get_count_non_send(self.get_queryset())
            data = {
                "all_device": all_device,
                "active_device": active_device,
                "non_send_data": non_send_data,
                "deactivate_device": deactivate_device
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError(detail='internal error: {}'.format(e.__str__()),
                                  code=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @swagger_auto_schema(
        responses={200: openapi.Response('OK', DeviceDataSerializer)})
    @action(methods=["GET"], detail=True, )
    def get_data(self, request, pk):
        device = self.get_object()
        queryset = HeadData.objects.filter(device_id=device.id)
        headdata = self.paginate_queryset(queryset)
        serializer = DeviceDataSerializer(headdata, many=True)
        return self.get_paginated_response(serializer.data)


class HeadViewSet(ModelViewSet):
    """
    برای عملیات بر روی head ها هست
    """
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [HeadListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name', 'chip_id']
    queryset = Head.objects.all()
    serializer_class = HeadSerializer

    def create(self, request, *args, **kwargs):
        res = super(HeadViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_head', request.user, get_object_or_404(Head, id=res.data['id']))
        assign_perm('hall.change_head', request.user, get_object_or_404(Head, id=res.data['id']))
        return res


class CompanyDetailViewSet(ListModelMixin, GenericViewSet):
    """for get detail for company (only available for super user)"""
    permission_classes = [IsSuperUser]
    queryset = Company.objects.all()
    serializer_class = CompanyDetailSerializer

    @swagger_auto_schema(
        responses={200: openapi.Response('OK', CompanyDetailSerializer)})
    def list(self, request, *args, **kwargs):
        try:
            data = {
                "all_company": len(Company.objects.all()),
                "active_company": len(Company.objects.filter(expire_service_time__gt=datetime.datetime.now()))
            }
            return Response(data=data, status=status.HTTP_200_OK)
        except Exception as e:
            raise ValidationError(detail=e.__str__(), code=status.HTTP_500_INTERNAL_SERVER_ERROR)
