import json

from django.conf import settings
from django.shortcuts import get_object_or_404

from hall.models import Device, Head
from mqtt.helpers.tasks import Mqtt
from parameter.models import DeviceParameter, HeadParameter


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


def save_device_parameter_on_message(client, userdata, msg):
    try:
        print("message arrived")
        chip_id = msg.topic.split("/")[-1]
        device = get_object_or_404(Device, chip_ip=chip_id)
        payload = json.loads(msg.payload.decode("utf-8"))
        for parameter in payload:
            if DeviceParameter.objects.filter(key=parameter, device_id=device.id):
                DeviceParameter.objects.filter(key=parameter, device_id=device.id).update(value=payload[parameter])
            else:
                DeviceParameter.objects.create(
                    key=parameter,
                    value=payload[parameter],
                    address=int(parameter[1:]),
                    device_id=device.id
                )
    except Exception as e:
        print("some error append -> {}".format(e.__str__()))
        pass


def save_device_parameter_on_connect(client, userdata, flags, rc, prob=None):
    print("user {} connected to broker".format(userdata))


def save_device_parameter_on_disconnect(rc, a, b, c):
    print("by :)")


def save_head_parameter_on_message(client, userdata, msg):
    try:
        print("message arrived")
        chip_id = msg.topic.split("/")[-1]
        device = get_object_or_404(Device, chip_ip=chip_id)
        payload = json.loads(msg.payload.decode("utf-8"))
        for head_code in payload:
            head = get_object_or_404(Head, head_code=int(head_code), device_id=device.id)
            for parameter in payload[head_code]:
                if HeadParameter.objects.filter(head_id=head.id, key=parameter):
                    HeadParameter.objects.filter(head_id=head.id, key=parameter).update(
                        value=payload[head_code][parameter])
                else:
                    HeadParameter.objects.create(
                        key=parameter,
                        value=payload[head_code][parameter],
                        head_id=head.id
                    )

    except Exception as e:
        print("some error append -> {}".format(e.__str__()))
        pass


def save_head_parameter_on_connect(client, userdata, flags, rc, prob=None):
    print("user {} connected to broker".format(userdata))


def save_head_parameter_on_disconnect(rc, a, b, c):
    print("by :)")
