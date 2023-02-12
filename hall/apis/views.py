from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from hall.apis.serializers import CompanySerializer, HallSerializer, ProductionSerializer, GroupSerializer, \
    DeviceSerializer, HeadSerializer
from hall.permissions import IsSuperUser
from hall.models import Company, Hall, Production, Group, Device, Head


class CompanyViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Company.objects.all()
    serializer_class = CompanySerializer


class HallViewSet(ModelViewSet):
    permission_classes = [IsAuthenticated]
    filter_backends = None
    queryset = Hall.objects.all()
    serializer_class = HallSerializer


class ProductionView(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Production.objects.all()
    serializer_class = ProductionSerializer


class GroupViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


class DeviceViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Device.objects.all()
    serializer_class = DeviceSerializer


class HeadViewSet(ModelViewSet):
    permission_classes = [IsSuperUser]
    queryset = Head.objects.all()
    serializer_class = HeadSerializer
