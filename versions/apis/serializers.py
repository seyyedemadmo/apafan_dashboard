from rest_framework.serializers import ModelSerializer

from versions.models import Version


class CreateVersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        exclude = ['created_at', 'next_version']

    def create(self, validated_data):
        past_version = Version.objects.filter(company=validated_data['company'].id, group=validated_data['group'],
                                              next_version=None, type=validated_data['type'])
        if past_version:
            now_version = Version.objects.create(**validated_data)
            past_version.update(next_version=now_version)
        else:
            Version.objects.create(**validated_data)
        return validated_data


class ListVersionSerializer(ModelSerializer):
    class Meta:
        model = Version
        fields = "__all__"
