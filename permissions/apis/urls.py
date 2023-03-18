from django.urls import path

from . import views

urlpatterns = [
    path('', views.GetUserPermissions.as_view({"get": "list"}), name='get all user permission'),
    path("<str:username>/add", views.AddUserPermissionView.as_view(), name="add_user_perm"),
    path("<str:username>/remove", views.RemoveUserPermissionView.as_view(), name='remove_user_perm'),
]
