"""Apafan_dashboard URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include, re_path
from django.utils import timezone

from rest_framework import permissions
from user.api import views as rest_view

from mqtt.aysinc_functions.functions import start_mqtt_data_listener, start_mqtt_parameter_listener, \
    start_mqtt_head_parameter_listener, start_mqtt_first_up_listener, start_mqtt_temp_device_listener

from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
    openapi.Info(
        title="Snippets API",
        default_version='v1',
        description="Test description",
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="contact@snippets.local"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path('api/user/', include('user.api.urls')),
    path('api/main/', include('hall.apis.urls')),
    path('api/parameter/', include('parameter.apis.urls')),
    #path('api/frameware/', include('frameware.apis.urls')),
    path('api/permissions/', include('permissions.apis.urls')),
    path('api/objectpermissions/', include('objectpermissions.apis.urls')),
    path('api/versions/', include('versions.apis.urls')),
    path('api/setting/', include('setting.apis.urls')),
    path('api/user-auth/', include('rest_framework.urls')),
    path('api/chart/', include('chart.apis.urls')),
    path('api/auth/token', rest_view.CustomObtainToken.as_view(), name='برای login , logout از سامانه'),
    path('api/auth/token/refresh', rest_view.CustomRefreshToken.as_view(), name='برای login , logout از سامانه'),
    re_path('api/doc/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    re_path('api/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

]

# start_mqtt_data_listener()

# start_mqtt_first_up_listener()

# for listen to receive parameter from device and head
# start_mqtt_parameter_listener()
# start_mqtt_head_parameter_listener()

# start_mqtt_temp_device_listener()
