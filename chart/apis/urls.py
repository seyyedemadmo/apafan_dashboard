from django.urls import path
from chart.apis import views

urlpatterns = [
    path("<int:id>/fields", views.ChartFieldAPIView.as_view({"get": "list"}), name='get_device_data_field')
]
