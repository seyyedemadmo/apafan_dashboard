from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAdminUser

from setting.apis.serializers import GlobalSettingSerializer
from setting.utils.generators import generate_setting_dict


class GlobalConfigView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        data = generate_setting_dict()
        serializer = GlobalSettingSerializer(data=data)
        if serializer.is_valid():
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
