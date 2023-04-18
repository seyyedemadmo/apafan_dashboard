from django.contrib.sessions.models import Session
from django.utils import timezone
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.viewsets import GenericViewSet, ModelViewSet
from rest_framework.mixins import UpdateModelMixin, RetrieveModelMixin
from rest_framework.exceptions import ValidationError
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.shortcuts import get_object_or_404

from permissions.permissions import IsAdminOrSuperUser
from user.api.serializers import RegisterUserSerializers, ListUserSerializers, UpdateUserSerializers, \
    RetrieveUserSerializers, ChangePasswordSerializers, SelfUserSerializers, SelfUserUpdateSerializers, \
    AdminUserSerializers, AdminCreateUserSerializers
from user.permissions import IsAdmin, IsSelf


class UserCreateListUpdateViewSet(ModelViewSet):
    permission_classes = [IsAdmin]
    filter_backends = [SearchFilter]
    search_fields = ['username', 'first_name', 'last_name', 'uuid']
    lookup_field = "username"

    def get_queryset(self):
        return get_user_model().objects.all().exclude(id=self.request.user.id)

    def get_serializer_class(self):
        if self.request.user.is_superuser:
            if self.action == "create":
                return AdminCreateUserSerializers
            else:
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
    permission_classes = [IsAuthenticated]
    queryset = get_user_model().objects.all()

    def get_object(self):
        return self.request.user

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return SelfUserSerializers
        else:
            return SelfUserUpdateSerializers


class ActiveUserCountAPIView(APIView):
    permission_classes = [IsAdminOrSuperUser]

    def get(self, request):
        all_user = len(get_user_model().objects.all())
        band_user = len(get_user_model().objects.filter(is_band=True))
        sessions = Session.objects.filter(expire_date__gte=timezone.now())
        uid_list = []

        # Build a list of user ids from that query
        for session in sessions:
            data = session.get_decoded()
            uid_list.append(data.get('_auth_user_id', None))
        active_user = len(get_user_model().objects.filter(id__in=uid_list))
        session_active = len(sessions)
        return Response(data={
            "active_user": active_user,
            "all_user": all_user,
            "band_user": band_user,
            "session_active": session_active
        }, status=status.HTTP_200_OK)
