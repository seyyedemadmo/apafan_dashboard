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
        if not mine_type[0] == "application/octet-stream":
            ValidationError("you must enter a .bin file")
        return attrs

    def create(self, validated_data):
        validated_data["next_version"] = None
        past_version = Version.objects.filter(company=validated_data['company'].id, group=validated_data['group'],
                                              next_version=None, type=validated_data['type'])
        if past_version:
            now_version = Version.objects.create(**validated_data)
            temp = now_version.copy()
            past_version.update(next_version_id=temp.id)
        else:
            Version.objects.create(**validated_data)
        return validated_data


class ListVersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"
