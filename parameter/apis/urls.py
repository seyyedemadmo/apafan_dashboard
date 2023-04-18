from django.urls import path
from rest_framework import routers

from parameter.apis.views import HeadParameterModelViewSet, DeviceParameterModelViewSet

router = routers.DefaultRouter()
router.register("head", HeadParameterModelViewSet, basename="head_parameter")
router.register("device", DeviceParameterModelViewSet, basename="device_parameter")

urlpatterns = [

              ] + router.urls
