from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError
from rest_framework import serializers


class RegisterUserSerializers(ModelSerializer):
    conf_password = serializers.CharField(required=True)

    class Meta:
        model = get_user_model()
        fields = ["username", 'password', 'is_admin', 'expire_time']

    def validate(self, attrs):
        if 'password' not in attrs.keys() or not attrs['password']:
            raise ValidationError("you must enter a password")

        if 'conf_password' not in attrs.keys() or not attrs['password']:
            raise ValidationError("you must enter a conf password")

        if attrs['password'] != attrs['conf_password']:
            raise ValidationError("password and password conf not match")

        if not validate_password(attrs['password']):
            raise ValidationError('weak password try other one')

        attrs.pop("conf_password")
        return attrs


class ListUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'expire_time', 'created_at', 'is_admin']
