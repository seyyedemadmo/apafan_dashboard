from rest_framework.exceptions import ValidationError
import json
from mqtt.helpers.tasks import Mqtt
from django.conf import settings


def send_parameter(topic: str, data: dict):
    try:
        mqtt_client = Mqtt(getattr(settings, "MQTT_ADDRESS", None), getattr(settings, "MQTT_PORT", None),
                           getattr(settings, "MQTT_USER"), getattr(settings, "MQTT_PASSWORD"))
        mqtt_client.run()
    except Exception as e:
        raise ValidationError("cant connect to mqtt broker")

    str_data = json.dumps(data)

    try:
        mqtt_client.send(topic, str_data)
    except Exception as e:
        ValidationError("cant send parameter to device")
