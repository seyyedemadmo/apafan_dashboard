from django.urls import path
from frameware.apis.views import FrameView, ParameterFileView

urlpatterns = [
    path("<str:c_id>/<str:f_id>/", FrameView.as_view(), name='frame_update'),
    path("<str:c_id>/<str:f_id>/", ParameterFileView.as_view(), name='parameter_file_update'),
]
