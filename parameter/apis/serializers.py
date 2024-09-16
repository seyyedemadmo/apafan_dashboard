from rest_framework import serializers

from django.conf import settings

from parameter.helpers.sender import send_parameter
from parameter.models import Parameter, ParameterType
from hall.models import Device


class ParameterTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ParameterType
        fields = '__all__'


class ParameterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Parameter
        exclude = ['updated_at', 'created_at', 'parameter_type']

    def validate(self, data):
        value = data.get('value')
        device_id = data.get('device_id')
        print(data)
        if not device_id:
            raise serializers.ValidationError("Device ID is required.")

        try:
            device = Device.objects.get(name=device_id)
        except Device.DoesNotExist:
            raise serializers.ValidationError("Invalid device ID.")

        device_type = device.device_type
        parameter_types = ParameterType.objects.filter(device_type=device_type)

        for parameter_type in parameter_types:
            valid_format = parameter_type.valid_types
            if self.is_valid_format(valid_format, value):
                data['parameter_type'] = parameter_type
                return data

        raise serializers.ValidationError('Invalid value format for the given device type.')

    def is_valid_format(self, valid_format, value_format):
        return self.dfs_validate(valid_format, value_format)

    def dfs_validate(self, valid_format, value_format):
        if isinstance(valid_format, dict):
            if not isinstance(value_format, dict) or set(valid_format.keys()) != set(value_format.keys()):
                return False
            for key, value_type in valid_format.items():
                if not self.dfs_validate(value_type, value_format[key]):
                    return False
        elif isinstance(valid_format, list):
            if not isinstance(value_format, list) or len(valid_format) != len(value_format):
                return False
            for i in range(len(valid_format)):
                if not self.dfs_validate(valid_format[i], value_format[i]):
                    return False
        else:
            if not isinstance(value_format, self.get_python_type(valid_format)):
                return False
        return True

    def get_python_type(self, type_name):
        if type_name == 'int':
            return int
        elif type_name == 'str':
            return str
        elif type_name == 'float':
            return float
        elif type_name == 'bool':
            return bool
        return None

    def create(self, validated_data):
        parameter = Parameter.objects.create(**validated_data)
        return parameter

    def update(self, instance, validated_data):
        super(ParameterSerializer, self).update(instance, validated_data)
        return instance

