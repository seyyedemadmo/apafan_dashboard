from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import SearchFilter
from rest_framework.mixins import CreateModelMixin, DestroyModelMixin, ListModelMixin
from rest_framework.viewsets import GenericViewSet
from rest_framework.permissions import AllowAny

from hall.permissions import IsSuperUser

from versions.models import Version
from versions.apis.serializers import ListVersionSerializer, CreateVersionSerializer


class CreateDestroyListVersionViewSet(ListModelMixin, CreateModelMixin, DestroyModelMixin, GenericViewSet):
    permission_classes = [IsSuperUser]
    filter_backends = [SearchFilter]
    search_fields = ['type']

    def get_serializer_class(self):
        if self.action == "list":
            return ListVersionSerializer
        return CreateVersionSerializer

    def get_queryset(self):
        return Version.objects.filter(**self.kwargs)

    @swagger_auto_schema(
        request_body=CreateVersionSerializer,
        consumes=['multipart/form-data'],  # Add this line to enable file uploads
    )
    def create(self, request, *args, **kwargs):
        return super(CreateDestroyListVersionViewSet, self).create(request,args,kwargs)

# class GetFilePath(ListModelMixin, GenericViewSet):
#     permission_classes = [AllowAny]
#     queryset = ""
#
#     def list(self, request, *args, **kwargs):
