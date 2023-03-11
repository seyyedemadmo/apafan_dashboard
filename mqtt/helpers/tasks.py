import json

from django.http import Http404
from django.shortcuts import get_object_or_404
from paho.mqtt.client import Client

from django.conf import settings

from device.models import HeadData
from hall.models import Head, Company


def default_on_connect(client, userdata, flags, rc, prob=None):
    print("device connected")


def default_on_massage(client, userdata, msg):
    with open("error.log", 'w') as f:
        try:
            print("message arrived", file=f)
            print('massage is :', msg.payload.decode("utf-8"), file=f)
            print("topic is " + msg.topic, file=f)
            data = json.loads(str(msg.payload.decode("utf-8")))
            topic = msg.topic
            chip_id = topic.split("/")[-1]
            company_id = topic.split("/")[-2]

            company = get_object_or_404(Company, id=company_id)

            head = get_object_or_404(Head, chip_ip=chip_id)

            if head not in Head.objects.filter(device__group__production__hall__company_id=company.id):
                print("head device not valid for this company", file=f)
                pass
            HeadData.objects.create(
                chip_id=chip_id,
                head_id=head.id,
                data=data
            )
        except Exception as e:
            print(e.__str__(), file=f)
            pass


def default_on_disconnect(rc, a, b, c):
    cli = Client()
    cli.connect('localhost', 1883)
    cli.publish('test', 'im done :)')
    cli.disconnect()


class Mqtt:
    def __init__(self, address, port, username=None, password=None, protocol=5, on_connect=None, on_massage=None,
                 on_disconnect=None, client_id=None):
        self.address = address
        self.port = port
        self.username = username
        self.password = password
        self.connect_function = on_connect if on_connect else default_on_connect
        self.massage_function = on_massage if on_massage else default_on_massage
        self.disconnect_function = on_disconnect if on_disconnect else default_on_disconnect
        self.client_id = client_id
        self.client = Client(protocol=protocol, client_id=self.client_id)
        self.client.username_pw_set(self.username, self.password) if self.username and self.password else None
        self.connect()

    def connect(self, version=5):
        rc = self.client.connect(self.address, self.port)
        if rc == 0:
            return True
        return False

    def send(self, topic, massage):
        return self.client.publish(topic, massage, qos=2)

    def listen(self, topic):
        return self.client.subscribe(topic)

    def run(self):
        self.client.on_connect = self.connect_function
        self.client.on_message = self.massage_function
        self.client.on_disconnect = self.disconnect_function
        self.client.loop_start()

    def stop(self):
        self.client.loop_stop()

    def disconnect(self):
        self.client.disconnect()
