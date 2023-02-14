from django.urls import path

from . import views

urlpatterns = [
    path('', views.GetUserPermissions.as_view({"get": "list"}), name='get all user permission')
]
