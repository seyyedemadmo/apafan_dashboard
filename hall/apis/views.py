from django.shortcuts import get_object_or_404
from django.forms.models import model_to_dict

from guardian.shortcuts import get_objects_for_user

from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action
from rest_framework.exceptions import ValidationError

from guardian.shortcuts import assign_perm

from Apafan_dashboard.authoraization import CustomAuthentication
from Apafan_dashboard.permissions import CustomDjangoObjectPermissions

from hall.apis.serializers import CompanySerializer, HallSerializer, ProductionSerializer, GroupSerializer, \
    DeviceSerializer, HeadSerializer
from hall.filters import *
from hall.permissions import IsSuperUser, CustomObjectPermission
from hall.models import Company, Hall, Production, Group, Device, Head


class CompanyViewSet(ModelViewSet):
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
        data = [ProductionSerializer(model).data for model in queryset]
        return Response(data=data, status=status.HTTP_200_OK)


class ProductionView(ModelViewSet):
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
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [GroupListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name']
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def create(self, request, *args, **kwargs):
        res = super(GroupViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_group', request.user, get_object_or_404(Group, id=res.data['id']))
        assign_perm('hall.change_group', request.user, get_object_or_404(Group, id=res.data['id']))
        return res


class DeviceViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [DeviceListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name', 'code']
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer

    def create(self, request, *args, **kwargs):
        res = super(DeviceViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_group', request.user, get_object_or_404(Group, id=res.data['id']))
        assign_perm('hall.change_group', request.user, get_object_or_404(Group, id=res.data['id']))
        return res


class HeadViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [HeadListObjectPermissionFilterBackend, SearchFilter]
    search_fields = ['name', 'chip_id']
    queryset = Head.objects.all()
    serializer_class = HeadSerializer

    def create(self, request, *args, **kwargs):
        res = super(HeadViewSet, self).create(request, *args, **kwargs)
        assign_perm('hall.view_group', request.user, get_object_or_404(Group, id=res.data['id']))
        assign_perm('hall.change_group', request.user, get_object_or_404(Group, id=res.data['id']))
        return res
