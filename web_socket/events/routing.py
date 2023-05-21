from django.urls import re_path

from . import consumers
from chart.events.consumers import ChartWebSocketConsumer

websocket_urlpatterns = [
    re_path(r"ws/head/", consumers.HeadConsumers.as_asgi()),
    re_path(r"ws/test/", ChartWebSocketConsumer.as_asgi()),
]
