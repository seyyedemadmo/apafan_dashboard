from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from device.apis.serializers import TempDeviceSerializers
from device.models import TempDevice


class ShowTempDeviceViewSet(ListModelMixin, GenericViewSet):
    """نمایش دستکاه های اماده اتصال"""
    permission_classes = [IsAuthenticated]
    serializer_class = TempDeviceSerializers
    queryset = TempDevice.objects.all()
