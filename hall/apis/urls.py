from django.urls import path, include

from rest_framework import routers

from hall.apis.views import HallViewSet, HeadViewSet, GroupViewSet, CompanyViewSet, DeviceViewSet, \
    ProductionView

router = routers.DefaultRouter()
router.register('company', CompanyViewSet, basename='company')
router.register('hall', HallViewSet, basename='hall')
router.register('head', HeadViewSet, basename='head')
router.register('group', GroupViewSet, basename='group')
router.register('production', ProductionView, basename='production')
router.register('device', DeviceViewSet, basename='device')

urlpatterns = [
                  path("temp_device/", include("device.apis.urls"))
              ] + router.urls
