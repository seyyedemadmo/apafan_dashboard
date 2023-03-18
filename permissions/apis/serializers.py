from django.contrib.auth.models import Permission
from rest_framework.serializers import ModelSerializer
from rest_framework import serializers

from permissions.models import PermissionProxy


class PermissionSerializer(ModelSerializer):
    class Meta:
        model = PermissionProxy
        fields = ['id', 'name', 'codename', 'translate']


class PermissionAddSerializer(serializers.Serializer):
    perms = serializers.ListSerializer(
        child=serializers.IntegerField()
    )

