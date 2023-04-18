from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet

from hall.permissions import IsSuperUser

from versions.models import Version
from versions.apis.serializers import ListVersionSerializer, CreateVersionSerializer


class CreateDestroyListVersionViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsSuperUser]
    filter_backends = [SearchFilter]
    search_fields = ['company', 'group']

    def get_serializer_class(self):
        if self.action == "list":
            return ListVersionSerializer
        return CreateVersionSerializer

    def get_queryset(self):
        return Version.objects.filter(**self.kwargs)
