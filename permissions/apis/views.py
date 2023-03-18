from rest_framework.mixins import ListModelMixin, CreateModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView

from django.conf import settings

from permissions.apis.serializers import PermissionSerializer
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


class AddUserPermission(CreateAPIView):
    permission_classes = [IsAdminOrSuperUser]
    serializer_class = None

    def create(self, request, *args, **kwargs):
        pass
