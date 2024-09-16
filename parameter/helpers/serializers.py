from rest_framework import serializers

from parameter.models import Parameter


class DeviceParameterSerializers(serializers.ModelSerializer):
    class Meta:
        model = Parameter
        exclude = ['device']



