from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from rest_framework.serializers import ModelSerializer
from rest_framework.exceptions import ValidationError

from user.models import User


class RegisterUserSerializers(ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ["username", 'password', 'is_admin', 'expire_time']
        extra_kwargs = {'password': {'write_only': True}}

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
        fields = ['username', 'email', 'expire_time', 'created_at', 'is_admin']
