from django.urls import path, include

from rest_framework import routers

from hall.apis.views import GroupViewSet, CompanyViewSet, DeviceViewSet, \
    CompanyDetailViewSet, DeviceTypeViewSet

router = routers.DefaultRouter()
router.register('company', CompanyViewSet, basename='company')
router.register('group', GroupViewSet, basename='group')
router.register('device', DeviceViewSet, basename='device')
router.register('device-type', DeviceTypeViewSet, basename='device type')
router.register('company-detail', CompanyDetailViewSet, basename="company detail for dashboard")

urlpatterns = [
                  path("temp_device/", include("device.apis.urls"))
              ] + router.urls
