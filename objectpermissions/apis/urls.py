from django.urls import path

from . import views

urlpatterns = [
    path("<str:model_name>/<str:username>/add", views.AddObjectPermissionView.as_view(), name='add_object_perm'),
    path("<str:model_name>/<str:username>/remmove", views.AddObjectPermissionView.as_view(), name='add_object_perm'),

]
