from rest_framework import routers

from device.apis.views import ShowTempDeviceViewSet

router = routers.DefaultRouter()
router.register("", ShowTempDeviceViewSet, basename="temp_show")

urlpatterns = [

              ] + router.urls
