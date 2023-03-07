from django.db import models


from hall.models import Head, Device

class HeadParameter(models.Model):
    key = models.CharField(null=False, blank=False, max_length=255)
    value = models.CharField(null=False, blank=False, max_length=255)  # TODO ask for type of value and required
    head = models.ForeignKey(Head, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['key', 'head']


class DeviceParameter(models.Model):
    key = models.CharField(null=False, blank=False, max_length=255)
    value = models.CharField(null=False, blank=False, max_length=255)  # TODO ask for type of value and required
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['key', 'device']
