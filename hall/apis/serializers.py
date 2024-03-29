from rest_framework.serializers import ModelSerializer
from rest_framework.serializers import Serializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from django.contrib.gis.geos import GEOSGeometry

from hall.models import Company, Hall, Production, Squad, Device, Head
from device.models import HeadData


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class HallSerializer(ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'

    def validate(self, attrs):
        geom = GEOSGeometry(attrs['geom'], srid=4326)
        if not attrs['company'].location.contains(geom):
            raise ValidationError('موقعیت مکانی سالن نباید بیرون از محدوده کارخانه باشد')
        return attrs


class ProductionSerializer(ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'

    def validate(self, attrs):
        geom = GEOSGeometry(attrs['geom'], srid=4326)
        if not attrs['hall'].geom.contains(geom):
            raise ValidationError('موقعیت مکانی خط تولید نباید بیرون از محدوده سالن مورد نظر باشد')
        return attrs


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Squad
        fields = '__all__'

    def validate(self, attrs):
        geom = GEOSGeometry(attrs['geom'], srid=4326)
        if not attrs['production'].geom.contains(geom):
            raise ValidationError('موقعیت مکانی گروه دستگاه ها نباید بیرون از محدوده خط تولید مورد نظر باشد')
        return attrs


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        exclude = ['created_at', 'updated_at', 'is_connected', 'last_connected']

    def validate(self, attrs):
        geom = GEOSGeometry(attrs['geom'], srid=4326)
        if not attrs['group'].geom.contains(geom):
            raise ValidationError('موقعیت مکانی دستگاه نباید بیرون از محدوده گروه مورد نظر باشد')
        return attrs


class HeadSerializer(ModelSerializer):
    class Meta:
        model = Head
        exclude = ['created_at', 'updated_at', 'is_connected', 'last_connected']


class WebSocketHeadSerializer(ModelSerializer):
    class Meta:
        model = Head
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
