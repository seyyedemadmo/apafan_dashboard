from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from rest_framework.decorators import action

from Apafan_dashboard.permissions import CustomDjangoObjectPermissions

from parameter.apis.serializers import HeadParameterSerializer, DeviceParameterSerializer
from parameter.filters import HeadParametersFilterBackend, DeviceParameterFilterBackend
from parameter.models import HeadParameter, DeviceParameter


class HeadParameterModelViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [HeadParametersFilterBackend, SearchFilter]
    search_fields = ['key']
    serializer_class = HeadParameterSerializer
    queryset = HeadParameter.objects.all()
    

class DeviceParameterModelViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [DeviceParameterFilterBackend, SearchFilter]
    search_fields = ['key']
    serializer_class = DeviceParameterSerializer
    queryset = DeviceParameter.objects.all()

