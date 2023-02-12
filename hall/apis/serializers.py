from rest_framework.serializers import ModelSerializer

from hall.models import Company, Hall, Production, Group, Device, Head


class CompanySerializer(ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class HallSerializer(ModelSerializer):
    class Meta:
        model = Hall
        fields = '__all__'


class ProductionSerializer(ModelSerializer):
    class Meta:
        model = Production
        fields = '__all__'


class GroupSerializer(ModelSerializer):
    class Meta:
        model = Group
        fields = '__all__'


class DeviceSerializer(ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class HeadSerializer(ModelSerializer):
    class Meta:
        model = Head
        fields = '__all__'
