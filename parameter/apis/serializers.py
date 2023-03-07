from rest_framework import serializers
from rest_framework import status

from parameter.models import HeadParameter, DeviceParameter


class HeadParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadParameter
        fields = "__all__"


class DeviceParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceParameter
        fields = "__all__"
