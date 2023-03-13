from rest_framework import serializers

from django.conf import settings

from parameter.helpers.sender import send_parameter
from parameter.models import HeadParameter, DeviceParameter


class HeadParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = HeadParameter
        fields = "__all__"

    def create(self, validated_data):
        head = validated_data['head']
        validated_data['head_code'] = head.head_code
        chip_id = head.device.chip_ip
        base_topic = getattr(settings, "MQTT_HEAD_PARAMETER_RECEIVE_TOPIC")
        topic = "/".join([base_topic, chip_id])
        send_parameter(topic, validated_data)
        _ = validated_data.pop['head_code']
        HeadParameter.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        head = validated_data['head']
        validated_data['head_code'] = head.head_code
        chip_id = head.device.chip_ip
        base_topic = getattr(settings, "MQTT_HEAD_PARAMETER_RECEIVE_TOPIC")
        topic = "/".join([base_topic, chip_id])
        send_parameter(topic, validated_data)
        _ = validated_data.pop['head_code']
        return super(HeadParameterSerializer, self).update(instance, validated_data)


class DeviceParameterSerializer(serializers.ModelSerializer):
    class Meta:
        model = DeviceParameter
        fields = "__all__"

    def create(self, validated_data):
        device = validated_data['device']
        base_topic = getattr(settings, "MQTT_DEVICE_PARAMETER_RECEIVE_TOPIC")
        topic = "/".join([base_topic, device.chip_ip])
        send_parameter(topic, validated_data)
        DeviceParameter.objects.create(**validated_data)
        return validated_data

    def update(self, instance, validated_data):
        device = validated_data['device']
        base_topic = getattr(settings, "MQTT_DEVICE_PARAMETER_RECEIVE_TOPIC")
        topic = "/".join([base_topic, device.chip_ip])
        send_parameter(topic, validated_data)
        return super(DeviceParameterSerializer, self).update(instance, validated_data)
