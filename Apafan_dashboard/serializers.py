from rest_framework import serializers
from rest_framework import status


class GlobalSerializer(serializers.Serializer):
    status = serializers.IntegerField()
    success = serializers.BooleanField()
    messages = serializers.ListField(child=serializers.JSONField())

    def __init__(self, serializer: serializers.BaseSerializer):
        self.results = serializer
