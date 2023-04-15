from rest_framework.serializers import ModelSerializer

from device.models import TempDevice


class TempDeviceSerializers(ModelSerializer):
    class Meta:
        model = TempDevice
        fields = "__all__"
