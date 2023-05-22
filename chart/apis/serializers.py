from rest_framework import serializers


class ChartFieldSerializer(serializers.Serializer):
    chip_ip = serializers.CharField()
    fields = serializers.ListSerializer(child=serializers.CharField())
