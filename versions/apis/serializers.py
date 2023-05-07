from rest_framework.exceptions import ValidationError
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from versions.models import Version


class CreateVersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        exclude = ['created_at', 'next_version']

    def validate(self, attrs):
        mine_type = attrs['file'].content_type
        if not mine_type == "application/octet-stream":
            raise ValidationError("you must enter a .bin file")
        return attrs


class ListVersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"
