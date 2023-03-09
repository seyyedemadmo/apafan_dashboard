from mqtt.helpers.tasks import Mqtt

from django.conf import settings
from mqtt.helpers.on_functions import *


def start_mqtt_listener():
    mqtt = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                getattr(settings, "MQTT_PORT", None),
                username=getattr(settings, "MQTT_USER", None),
                password=getattr(settings, "MQTT_PASSWORD", None)
                )
    mqtt.listen(getattr(settings, "BASE_MQTT_SUBSCRIBE_TOPIC", None))
    mqtt.run()


def listen_to_device():
    mqtt = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                getattr(settings, "MQTT_PORT", None),
                username=getattr(settings, "MQTT_USER", None),
                password=getattr(settings, "MQTT_PASSWORD", None)
                )
    mqtt.listen(getattr(settings, "MQTT_TEMP_TOPIC", None))
    mqtt.massage_function = send_data_parameter_on_message
    mqtt.connect_function = send_data_parameter_on_connect
    mqtt.disconnect_function = send_data_parameter_on_disconnect
    mqtt.run()
