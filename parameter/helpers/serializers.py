from rest_framework import serializers

from parameter.models import DeviceParameter, HeadParameter


class DeviceParameterSerializers(serializers.ModelSerializer):
    class Meta:
        model = DeviceParameter
        exclude = ['device']


class HeadParameterSerializers(serializers.ModelSerializer):
    class Meta:
        model = HeadParameter
        exclude = ['head']
