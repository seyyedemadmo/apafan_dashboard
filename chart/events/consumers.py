# consumers.py
import json
import time
from threading import Thread, Event
from channels.generic.websocket import WebsocketConsumer
from django.shortcuts import get_object_or_404

from hall.models import Device


class ChartWebSocketConsumer(WebsocketConsumer):

    def __init__(self, ):
        super(ChartWebSocketConsumer, self).__init__(self)
        self.data = {}
        self.event = Event()
        self.device = None
        self.send_data_thread = Thread(target=self.send_data)

    def connect(self):
        if self.scope['user'].is_authenticated:
            self.accept()
            self.send_data_thread.start()
        else:
            self.close()

    def receive(self, text_data=None, bytes_data=None):
        try:
            self.data = json.loads(text_data)
            self.device = get_object_or_404(Device, chip_ip=self.data['chip_ip'])

        except Exception as e:
            print(e.__str__())

    def disconnect(self, code):
        if self.scope['user'].is_authenticated:
            self.scope['user'].update_uuid()
        self.scope['client'] = None
        self.event.set()
        self.close()

    def send_data(self):
        while True:
            if self.event.is_set():
                break
            self.send(json.dumps(self.get_data_now()))
            time.sleep(1)

    def get_data_now(self):
        if self.device:
            device_last_data_send = self.device.headdata_set.latest("receive_at").data
            return {key: value for key, value in device_last_data_send.items() if key in self.data['fields']}
        return {}
