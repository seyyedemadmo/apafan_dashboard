from hall.models import Device, Head
from parameter.helpers.serializers import HeadParameterSerializers, DeviceParameterSerializers


class Convertor:
    def __init__(self, device: Device = None, head: Head = None):
        if not device and not head:
            raise ValueError("you must enter one of head or device instance to start convert")
        if head and device:
            raise ValueError("you should enter one type of instance")
        self.head = head
        self.device = device

    def get_all_head_parameter(self):
        if not self.head:
            raise ValueError('cant get data from None data of head')
        serializer = HeadParameterSerializers(self.head.headparameter_set.all(), many=True)
        return serializer.data

    def get_all_device_parameter(self):
        if not self.device:
            raise ValueError('cant get data from None data of device')
        serializer = DeviceParameterSerializers(self.device.deviceparameter_set.all(), many=True)
        return serializer.data

    def convert(self):
        if self.device:
            return self.get_all_device_parameter()
        elif self.head:
            return self.get_all_head_parameter()
        else:
            raise ValueError("you should Enter one of head or device")
