import json

from django.conf import settings
from django.shortcuts import get_object_or_404

from hall.models import Device
from mqtt.helpers.tasks import Mqtt


def send_data_parameter_on_connect(client, userdata, flags, rc, prob=None):
    print("connected to mqtt topic of temp device")


def send_parameter(data: dict):
    try:
        send_client = Mqtt(getattr(settings, "MQTT_ADDRESS", None), getattr(settings, "MQTT_PORT", None))
        base_topic = getattr(settings, "MQT_BASE_SEND_TOPIC", None)
        token = data['token']
        chip_id = data["chip_id"]
        topic = "/".join([base_topic, chip_id, token])
        send_data = None  # todo some function that generate parameter for each device
        send_client.send(topic, send_data)
    except Exception as e:
        print("we have unexpected error. detail: {}".format(e.__str__()))
        pass


def send_data_parameter_on_message(client, userdata, msg):
    try:
        chip_id = msg.topic.split("/")[-1]
        device = get_object_or_404(Device, chip_ip=chip_id)
        if device:
            data = json.loads(msg.payload.decode("utf-8"))
            send_parameter(data)
    except Exception as e:
        print("we have unexpected error. detail: {}".format(e.__str__()))
        pass


def send_data_parameter_on_disconnect(rc, a, b, c):
    print("disconnected from mqtt topic of temp device")
