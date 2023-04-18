from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.apps import apps
from django.conf import settings

from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from objectpermissions.apis.serializers import AddObjectPermissionSerializer
from permissions.models import PermissionProxy
from permissions.permissions import IsAdminOrSuperUser


class AddObjectPermissionView(CreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = AddObjectPermissionSerializer
    queryset = ""

    def post(self, request, *args, **kwargs):
        all_model = getattr(settings, "OBJECT_PERMISSION_MODEL", None)
        if not self.kwargs['model_name'] in all_model:
            raise ValidationError("cant add object permission for this model")
        try:
            model = apps.get_model("hall", self.kwargs['model_name'])
        except Exception as e:
            raise ValidationError("this model you pass is not allowed")
        try:
            user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        except Exception as e:
            raise ValidationError("invalid username")

        serializer = AddObjectPermissionSerializer(data=request.data, many=True)
        serializer.context['user'] = user
        serializer.context['model'] = model
        if serializer.is_valid():
            serializer.save()
            return Response('object permission add successfully', status=status.HTTP_201_CREATED)
        return Response('fail to add object permission error is: {}'.format(serializer.errors))


class RemoveObjectPermissionView(CreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = AddObjectPermissionSerializer
    queryset = ""

    def post(self, request, *args, **kwargs):
        all_model = getattr(settings, "OBJECT_PERMISSION_MODEL", None)
        if not self.kwargs['model_name'] in all_model:
            raise ValidationError("cant add object permission for this model")
        try:
            model = apps.get_model("hall", self.kwargs['model_name'])
        except Exception as e:
            raise ValidationError("this model you pass is not allowed")
        try:
            user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
        except Exception as e:
            raise ValidationError("invalid username")

        serializer = RemoveObjectPermissionSerializer(data=request.data, many=True)
        serializer.context['user'] = user
        serializer.context['model'] = model
        if serializer.is_valid():
            serializer.save()
            return Response('object permission add successfully', status=status.HTTP_201_CREATED)
        return Response('fail to add object permission error is: {}'.format(serializer.errors))
