from mqtt.helpers.tasks import Mqtt

from django.conf import settings
from mqtt.helpers.on_functions import *


def start_mqtt_data_listener():
    mqtt = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                getattr(settings, "MQTT_PORT", None),
                username=getattr(settings, "MQTT_USER", None),
                password=getattr(settings, "MQTT_PASSWORD", None),
                client_id="data_listener"
                )
    mqtt.listen(getattr(settings, "BASE_MQTT_SUBSCRIBE_TOPIC", None))
    mqtt.run()


def start_mqtt_first_up_listener():
    mqtt = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                getattr(settings, "MQTT_PORT", None),
                username=getattr(settings, "MQTT_USER", None),
                password=getattr(settings, "MQTT_PASSWORD", None),
                client_id="temp_device_listener"
                )
    mqtt.listen(getattr(settings, "MQTT_TEMP_TOPIC", None))
    mqtt.massage_function = send_data_parameter_on_message
    mqtt.connect_function = send_data_parameter_on_connect
    mqtt.disconnect_function = send_data_parameter_on_disconnect
    mqtt.run()


def start_mqtt_parameter_listener():
    client = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                  getattr(settings, "MQTT_PORT", None),
                  username=getattr(settings, "MQTT_USER", None),
                  password=getattr(settings, "MQTT_PASSWORD", None),
                  client_id="device_parameter_listener"
                  )
    client.listen(getattr(settings, "MQTT_DEVICE_PARAMETER_SEND_TOPIC", None))
    client.connect_function = save_device_parameter_on_connect
    client.massage_function = save_device_parameter_on_message
    client.run()


def start_mqtt_head_parameter_listener():
    client = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                  getattr(settings, "MQTT_PORT", None),
                  username=getattr(settings, "MQTT_USER", None),
                  password=getattr(settings, "MQTT_PASSWORD", None),
                  client_id="head_parameter_listener"
                  )
    client.listen(getattr(settings, "MQTT_HEAD_PARAMETER_SEND_TOPIC", None))
    client.connect_function = save_head_parameter_on_connect
    client.massage_function = save_head_parameter_on_message
    client.run()


def start_mqtt_temp_device_listener():
    client = Mqtt(getattr(settings, "MQTT_ADDRESS", None),
                  getattr(settings, "MQTT_PORT", None),
                  username=getattr(settings, "MQTT_USER", None),
                  password=getattr(settings, "MQTT_PASSWORD", None),
                  client_id="temp_device_listener"
                  )
    client.listen("AtiBinCo/Apafan/company/device/temp/#")
    client.connect_function = save_head_parameter_on_connect
    client.massage_function = save_temp_device_on_message
    client.run()
