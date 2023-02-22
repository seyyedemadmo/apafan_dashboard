from mqtt.helpers.tasks import Mqtt

from django.conf import settings


def start_mqtt_listener():
    mqtt = Mqtt(getattr(settings, "MQTT_ADDRESS", None), getattr(settings, "MQTT_PORT", None))
    mqtt.listen(getattr(settings, "BASE_MQTT_SUBSCRIBE_TOPIC", None))
    mqtt.run()
