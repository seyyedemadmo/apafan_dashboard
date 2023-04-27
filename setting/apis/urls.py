from django.urls import path

from . import views

urlpatterns = [
    path('show', views.GlobalConfigView.as_view(), name='show_setting'),
]
