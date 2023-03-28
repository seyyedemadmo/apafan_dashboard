from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from guardian.shortcuts import assign_perm, remove_perm

from permissions.models import PermissionProxy


class AddObjectPermissionSerializer(serializers.Serializer):
    perm = serializers.PrimaryKeyRelatedField(queryset=PermissionProxy.objects.all())
    instance = serializers.IntegerField()

    def validate(self, attrs):
        if not self.context['model'].objects.filter(id=attrs['instance']).exists():
            raise ValidationError('invalid instance')
        return attrs

    def create(self, validated_data):
        model = self.context['model']
        user = self.context['user']
        instance = model.objects.filter(id=validated_data['instance'])
        perm = PermissionProxy.objects.filter(id=validated_data['perm'])
        assign_perm(perm.first(), user, instance.first())
        return validated_data


class RemoveObjectPermissionSerializer(serializers.Serializer):
    perm = serializers.PrimaryKeyRelatedField(queryset=PermissionProxy.objects.all())
    instance = serializers.IntegerField()

    def validate(self, attrs):
        if not self.context['model'].objects.filter(id=attrs['instance']).exists():
            raise ValidationError('invalid instance')
        return attrs

    def create(self, validated_data):
        model = self.context['model']
        user = self.context['user']
        instance = model.objects.filter(id=validated_data['instance'])
        perm = PermissionProxy.objects.filter(id=validated_data['perm'])
        remove_perm(perm.first(), user, instance.first())
        return validated_data
