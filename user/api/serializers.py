from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer, Serializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers

from user.models import User


class RegisterUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", 'password', 'is_admin', 'expire_time', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True},
                        'first_name': {'required': True},
                        'last_name': {'required': True},
                        }

    def validate(self, attrs):
        if 'password' not in attrs.keys() or not attrs['password']:
            raise ValidationError("you must enter a password")

        if validate_password(attrs['password']):
            raise ValidationError('weak password try other one')
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            expire_time=validated_data['expire_time'],
            is_admin=validated_data['is_admin'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class ListUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'expire_time', 'created_at', 'first_name', 'last_name']


class RetrieveUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'expire_time', 'created_at', 'is_admin', 'is_superuser', 'last_login',
                  'first_name', 'last_name']


class UpdateUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['email', 'expire_time', 'is_admin', 'first_name', 'last_name']


class ChangePasswordSerializers(Serializer):
    old_password = serializers.CharField(write_only=True, required=True)
    new_password = serializers.CharField(required=True)
    conf_password = serializers.CharField(required=True)


class SelfUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email', 'username', 'last_login']


class SelfUserUpdateSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']
