from django.urls import path
from frameware.apis.views import FrameView

urlpatterns = [
    path("<str:c_id>/<str:f_id>/", FrameView.as_view(), name='frame_update'),
]
