from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status

from frameware.enums import company_map, version_map, parameter_group


class FrameView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, c_id, f_id):
        c_id = self.kwargs['c_id']
        f_id = self.kwargs['f_id']
        path = "files/{}/tem/.pio/build/esp32doit-devkit-v1/{}".format(company_map[c_id], version_map[f_id])
        data = {"file": path}
        return Response(data=data, status=status.HTTP_200_OK)


class ParameterFileView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, c_id, f_id, v_id):
        c_id = self.kwargs['c_id']
        f_id = self.kwargs['f_id']
        v_id = self.kwargs['v_i']
        path = "files/{}/tem/data/{}/{}".format(company_map[c_id], version_map[f_id], parameter_group[v_id])
        data = {"file": path,
                "version": 5}
        return Response(data=data, status=status.HTTP_200_OK)
