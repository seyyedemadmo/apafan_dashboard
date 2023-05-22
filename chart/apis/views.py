from django.shortcuts import get_object_or_404
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework import status
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from rest_framework.viewsets import ViewSet

from chart.apis.serializers import ChartFieldSerializer

from hall.models import Device


class ChartFieldAPIView(ViewSet):
    @swagger_auto_schema(
        responses={200: openapi.Response('OK', ChartFieldSerializer)})
    def list(self, request, id):
        device = get_object_or_404(Device, id=id)
        try:
            last_data_send = device.headdata_set.latest("receive_at").data
        except Exception as e:
            raise NotFound("this device dont send any data yet", code=status.HTTP_400_BAD_REQUEST)
        ans = [field for field in last_data_send.keys() if type(last_data_send[field]) != str]
        data = {
            "chip_ip": device.chip_ip,
            'fields': ans
        }
        serializer = ChartFieldSerializer(data=data)
        serializer.is_valid(raise_exception=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)
