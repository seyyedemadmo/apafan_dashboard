from rest_framework.viewsets import GenericViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin

from django.contrib.auth import get_user_model

from user.api.serializers import RegisterUserSerializers, ListUserSerializers
from user.permissions import IsAdmin

from Apafan_dashboard.authoraization import CustomAuthentication


class UserModelViewSet(CreateModelMixin, ListModelMixin, GenericViewSet):
    permission_classes = [IsAdmin]
    authentication_classes = [CustomAuthentication]

    def get_queryset(self):
        return get_user_model().objects.all().exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.action == 'create':
            return RegisterUserSerializers
        else:
            return ListUserSerializers
