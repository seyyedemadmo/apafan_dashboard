from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
import json
from parameter.helpers.sender import send_parameter

from Apafan_dashboard.permissions import CustomDjangoObjectPermissions
from hall.models import Device
from mqtt.helpers.tasks import Mqtt

from parameter.apis.serializers import ParameterSerializer, ParameterTypeSerializer
from parameter.filters import HeadParametersFilterBackend, DeviceParameterFilterBackend
from parameter.models import Parameter, ParameterType
from hall.apis.serializers import DeviceSerializer


class ParameterModelViewSet(ModelViewSet):
    queryset = Parameter.objects.all()
    serializer_class = ParameterSerializer
    permission_classes = [CustomDjangoObjectPermissions]
    # search_fields = ['key']
    # filter_backends = [HeadParametersFilterBackend, SearchFilter]

    @action(methods=['POST'], detail=False, url_path="create")
    def create_device_parameter(self, request, *args, **kwargs):
        try:
            device = get_object_or_404(Device, id=request.data['device_id'])
            device_base_topic = getattr(settings, 'MQTT_DEVICE_PARAMETER_UPDATE_TOPIC', None)
            device_topic = "/".join([device_base_topic, device.chip_ip])

            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                print("yes")
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"detail": 'we have some error in update parameter: {}'.format(e.__str__())},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['PUT'], detail=False, url_path="(?P<device_id>[^/.])/update")
    def update_device_parameter(self, request, *args, **kwargs):
        try:
            device = get_object_or_404(Device, id=kwargs.get("device_id"))
            device_base_topic = getattr(settings, 'MQTT_DEVICE_PARAMETER_UPDATE_TOPIC', None)
            device_topic = "/".join([device_base_topic, device.chip_ip])

            parameter = Parameter.objects.get(device_id=kwargs.get("device_id"))
            serializer = self.get_serializer(instance=parameter, data=request.data)
            if serializer.is_valid():
                serializer.save()
                send_parameter(device_topic, request.data)
                return Response(data=serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(data={"detail": 'we have some error in update parameter: {}'.format(e.__str__())},
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class ParameterTypeModelViewSet(ModelViewSet):
    queryset = ParameterType.objects.all()
    serializer_class = ParameterTypeSerializer
    permission_classes = [CustomDjangoObjectPermissions]