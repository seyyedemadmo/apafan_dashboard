from rest_framework.mixins import ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import IsAuthenticated

from django.conf import settings

from permissions.apis.serializers import PermissionSerializer
from permissions.models import PermissionProxy


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
