from django.db import models

from hall.models import Device, Squad, DeviceType


class ParameterType(models.Model):
    name = models.CharField(null=False, blank=False, max_length=225)
    valid_types = models.JSONField(null=False, blank=False, max_length=100)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name


class Parameter(models.Model):
    name = models.CharField(null=False, blank=False, max_length=225)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    device_id = models.OneToOneField(Device, on_delete=models.CASCADE)
    value = models.JSONField(null=False, blank=False)
    parameter_type = models.ForeignKey(ParameterType, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


