from rest_framework.exceptions import ValidationError

import json

from mqtt.helpers.tasks import Mqtt

from django.conf import settings


def send_parameter(topic: str, data: dict):
    try:
        mqtt_client = Mqtt(getattr(settings, "MQTT_ADDRESS", None), getattr(settings, "MQTT_PORT", None))
    except Exception as e:
        raise ValidationError("cant connect to mqtt broker")

    send_data = {
        "key": data['key'],
        "address": data['address'] if "address" in data.keys() else data["main_add"],
        "value": data['value'],
        "is_head": False if 'device' in data.keys() else False,
        "head_code": data['sub_add'] if "sub_add" in data.keys() else None
    }
    str_data = json.dumps(send_data)

    try:
        mqtt_client.send(topic, str_data)
    except Exception as e:
        ValidationError("cant send parameter to device")
