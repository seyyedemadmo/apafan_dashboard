from django.urls import path
from rest_framework import routers

from parameter.apis.views import ParameterModelViewSet, ParameterTypeModelViewSet

router = routers.DefaultRouter()
router.register(r"param", ParameterModelViewSet, basename="parameter")
router.register(r"param-type", ParameterTypeModelViewSet, basename="parameter type")

urlpatterns = [

              ] + router.urls