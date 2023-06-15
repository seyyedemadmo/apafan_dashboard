from django.conf import settings
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter

from Apafan_dashboard.permissions import CustomDjangoObjectPermissions
from hall.models import Device
from mqtt.helpers.tasks import Mqtt

from parameter.apis.serializers import HeadParameterSerializer, DeviceParameterSerializer
from parameter.filters import HeadParametersFilterBackend, DeviceParameterFilterBackend
from parameter.models import HeadParameter, DeviceParameter


class HeadParameterModelViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [HeadParametersFilterBackend, SearchFilter]
    search_fields = ['key']
    serializer_class = HeadParameterSerializer

    def get_queryset(self):
        return HeadParameter.objects.filter(head_id=self.kwargs.get("pk"))


class DeviceParameterModelViewSet(ModelViewSet):
    permission_classes = [CustomDjangoObjectPermissions]
    filter_backends = [DeviceParameterFilterBackend, SearchFilter]
    search_fields = ['key']
    serializer_class = DeviceParameterSerializer

    def get_queryset(self):
        return DeviceParameter.objects.filter(device_id=self.kwargs.get('pk'))

    @action(methods=['GET'], detail=False)
    def update_device_parameter(self, request, pk):
        try:
            device = get_object_or_404(Device, chip_ip=self.kwargs.get('pk'))

            device_base_topic = getattr(settings, 'MQTT_DEVICE_PARAMETER_UPDATE_TOPIC', None)

            device_topic = "/".join([device_base_topic, device.chip_ip])

            client = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                          getattr(settings, "MQTT_PORT", None),
                          username=getattr(settings, "MQTT_USER", None),
                          password=getattr(settings, "MQTT_PASSWORD", None)
                          )
            client.send(device_topic, '1')

            return Response(data={"detail": 'update parameter successful'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data={"detail": 'we have some error in update parameter: {}'.format(e.__str__())},
                   status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    @action(methods=['GET'], detail=False)
    def update_head_parameter(self, request, pk):
        try:
            device = get_object_or_404(Device, chip_ip=self.kwargs.get('pk'))

            device_base_topic = getattr(settings, 'MQTT_HEAD_PARAMETER_UPDATE_TOPIC', None)

            device_topic = "/".join([device_base_topic, device.chip_ip])

            client = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                          getattr(settings, "MQTT_PORT", None),
                          username=getattr(settings, "MQTT_USER", None),
                          password=getattr(settings, "MQTT_PASSWORD", None)
                          )
            client.send(device_topic, '1')

            return Response(data='update parameter successful', status=status.HTTP_200_OK)
        except Exception as e:
            return Response(data='we have some error in update parameter: {}'.format(e.__str__()),
                            status=status.HTTP_500_INTERNAL_SERVER_ERROR)
