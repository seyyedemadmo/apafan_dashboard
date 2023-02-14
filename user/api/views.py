from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import CreateModelMixin, ListModelMixin, UpdateModelMixin, RetrieveModelMixin
from rest_framework.exceptions import ValidationError

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from user.api.serializers import RegisterUserSerializers, ListUserSerializers, UpdateUserSerializers, \
    RetrieveUserSerializers, ChangePasswordSerializers, SelfUserSerializers, SelfUserUpdateSerializers, \
    AdminUserSerializers
from user.permissions import IsAdmin, IsSelf


class UserCreateListUpdateViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    lookup_field = "username"

    def get_queryset(self):
        return get_user_model().objects.all().exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            return AdminUserSerializers
        else:
            if self.action == 'list':
                return ListUserSerializers
            elif self.action == 'create':
                return RegisterUserSerializers
            elif self.action == 'retrieve':
                return RetrieveUserSerializers
            else:
                return UpdateUserSerializers

    def get_object(self):
        username = self.kwargs['username']
        return get_object_or_404(get_user_model(), username=username)


class ChangeUserPasswordViewSet(UpdateModelMixin, GenericViewSet):
    permission_classes = [IsAdmin | IsSelf]
    lookup_field = 'username'
    serializer_class = ChangePasswordSerializers
    queryset = ""

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.kwargs['username'])

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        if not user.check_password(request.data['old_password']):
            raise ValidationError("not allowed password for user")
        if request.data['new_password'] != request.data['conf_password']:
            raise ValidationError('password not match')
        try:
            validate_password(request.data['new_password'])
            user.set_password(request.data['new_password'])
            user.save()
            return Response("password successfuly changed", status=status.HTTP_200_OK)

        except ValidationError as ve:
            raise ValidationError("new password not valid")


class SelfUserViewSet(RetrieveModelMixin, UpdateModelMixin, GenericViewSet):
    permission_classes = [IsSelf]
    queryset = get_user_model().objects.all()
    lookup_field = 'username'

    def get_object(self):
        return get_object_or_404(get_user_model(), username=self.request.user.username)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SelfUserSerializers
        else:
            return SelfUserUpdateSerializers
