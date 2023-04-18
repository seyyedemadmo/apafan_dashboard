from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.exceptions import APIException

from django.conf import settings

from guardian.shortcuts import assign_perm, remove_perm

import user
from permissions.apis.serializers import PermissionSerializer, PermissionAddSerializer
from permissions.models import PermissionProxy
from permissions.permissions import IsAdminOrSuperUser


class GetUserPermissions(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer

    def get_queryset(self):
        if self.request.user.is_superuser:
            return PermissionProxy.objects.all()
        elif self.request.user.is_admin:
            return PermissionProxy.objects.filter(
                content_type__model__in=getattr(settings, "ADMIN_USER_PERMISSIONS", None))
        else:
            return PermissionProxy.objects.filter(user=self.request.user)


class AddUserPermissionView(CreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = PermissionAddSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
            perms = PermissionProxy.objects.filter(id__in=self.request.data['perms'])
            for perm in perms:
                assign_perm(perm, user)
            return Response(data='permissions added successfully', status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException("some error happened in server -> {}".format(e.__str__()))


class RemoveUserPermissionView(CreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = PermissionAddSerializer

    def create(self, request, *args, **kwargs):
        try:
            user = get_object_or_404(get_user_model(), username=self.kwargs['username'])
            perms = PermissionProxy.objects.filter(id__in=self.request.data['perms'])
            for perm in perms:
                remove_perm(perm, user)
            return Response(data='permissions removed successfully', status=status.HTTP_200_OK)
        except Exception as e:
            raise APIException("some error happened in server -> {}".format(e.__str__()))


class AllPermissionsViewSet(ListModelMixin, GenericViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = PermissionSerializer
    queryset = PermissionProxy.objects.all()