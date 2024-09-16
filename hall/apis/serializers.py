from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from django.contrib.gis.geos import GEOSGeometry

from hall.models import Company, Squad, Device, DeviceType
from device.models import HeadData


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', 'is_connected', 'last_connected', 'status', 'command']

    def validate(self, attrs):
        geom = GEOSGeometry(attrs['geom'], srid=4326)
        if not attrs['group'].geom.contains(geom):
            raise ValidationError('موقعیت مکانی دستگاه نباید بیرون از محدوده گروه مورد نظر باشد')
        return attrs


class WebSocketHeadSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', ]
        depth = 1


class CompanyDetailSerializer(Serializer):
    all_company = serializers.IntegerField()
    active_company = serializers.IntegerField()


class DeviceDetailSerialzier(Serializer):
    all_device = serializers.IntegerField()
    active_device = serializers.IntegerField()
    non_send_data = serializers.IntegerField()
    deactivate_device = serializers.IntegerField()


class DeviceDataSerializer(ModelSerializer):
    class Meta:
        model = HeadData
        fields = "__all__"


class DeviceTypeSerializer(ModelSerializer):
    class Meta:
        model = DeviceType
        fields = "__all__"
