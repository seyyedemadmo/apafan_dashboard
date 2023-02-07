from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin

from django.contrib.auth import get_user_model

from user.api.serializers import RegisterUserSerializers, ListUserSerializers
from user.permissions import IsAdmin


class UserModelViewSet(CreateModelMixin, GenericViewSet):
    permission_classes = [IsAdmin]

    def get_queryset(self):
        return get_user_model().objects.all().exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializers
        else:
            return ListUserSerializers
