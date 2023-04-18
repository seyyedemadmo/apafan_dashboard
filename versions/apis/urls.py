from django.urls import path, include

from rest_framework import routers

from versions.apis.views import CreateDestroyListVersionViewSet

router = routers.DefaultRouter()
router.register("", CreateDestroyListVersionViewSet, basename='version_api')

urlpatterns = [
              ] + router.urls
