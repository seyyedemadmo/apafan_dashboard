from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from django.conf import settings


class GlobalSettingSerializer(serializers.Serializer):
    allow_host = serializers.ListSerializer(child=serializers.CharField())
    debug = serializers.BooleanField()
    swagger = serializers.BooleanField()
    expire_session = serializers.FloatField()
    expire_when_tab_close = serializers.BooleanField()
    default_paginate_size = serializers.IntegerField()