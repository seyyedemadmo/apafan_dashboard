from rest_framework import serializers

from django.conf import settings

from parameter.helpers.sender import send_parameter
from parameter.models import HeadParameter, DeviceParameter


class HeadParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadParameter
        fields = "__all__"


class DeviceParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceParameter
        fields = "__all__"

    def create(self, validated_data):
        device = validated_data['device']
        base_topic = getattr(settings, "MQTT_PARAMETER_SEND_TOPIC")
        topic = "/".join([base_topic, device.chip_ip])
        send_parameter(topic, validated_data)
        DeviceParameter.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        device = validated_data['device']
        base_topic = getattr(settings, "MQTT_PARAMETER_SEND_TOPIC")
        topic = "/".join([base_topic, device.chip_ip])
        send_parameter(topic, validated_data)
        return super(DeviceParameterSerializer, self).update(instance, validated_data)
