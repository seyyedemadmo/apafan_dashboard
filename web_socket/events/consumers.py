import json

from channels.generic.websocket import WebsocketConsumer
from django.contrib.auth import get_user_model

from django.http import Http404
from django.shortcuts import get_object_or_404
from django.contrib.auth.models import AnonymousUser

from hall.models import Head
from hall.apis.serializers import WebSocketHeadSerializer

from user.models import User
import uuid

user = User.objects.filter()


class HeadConsumers(WebsocketConsumer):
    def connect(self):
        headers = dict(self.scope['headers'])
        if b'auth-uuid' in headers:
            uid = headers[b'auth-uuid']
            try:
                self.user = get_user_model().objects.get(uuid=uid.decode('utf-8'))
                self.accept()
            except:
                self.user = AnonymousUser()
                self.close(code='invalid uuid')

        else:
            self.user = AnonymousUser()
            self.close(code="you should enter uuid header")

    def disconnect(self, code):
        if not self.user.is_anonymous:
            self.user.uuid = uuid.uuid4().__str__()
            self.user.save()

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
