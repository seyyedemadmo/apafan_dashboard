import json

from channels.generic.websocket import WebsocketConsumer

from django.http import Http404
from django.shortcuts import get_object_or_404

from hall.models import Head
from hall.apis.serializers import WebSocketHeadSerializer


class HeadConsumers(WebsocketConsumer):
    def connect(self):
        self.user = self.scope['user']
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        head = get_head(text_data)
        serializer = WebSocketHeadSerializer(head)
        data = serializer.data
        data['last_data'] = str(get_last_data(head)) if get_last_data(head) else None
        self.send(text_data=json.dumps(data))


def get_head(pk: int):
    try:
        return get_object_or_404(Head, id=pk)
    except Http404 as e:
        return None


def get_last_data(head: Head):
    try:
        return head.headdata_set.order_by("receive_at").last().receive_at
    except:
        return None
