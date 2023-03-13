from django.db import models

from hall.models import Head, Device


class HeadParameter(models.Model):
    key = models.CharField(null=False, blank=False, max_length=255)
    sub_add = models.IntegerField(null=False, blank=False, max_length=255)
    main_add = models.IntegerField(null=False, blank=False, max_length=511)
    value = models.IntegerField(null=False, blank=False, max_length=65545)
    head = models.ForeignKey(Head, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['key', 'head']


class DeviceParameter(models.Model):
    key = models.CharField(null=False, blank=False, max_length=255)
    address = models.IntegerField(null=False, blank=False, max_length=511)
    value = models.IntegerField(null=False, blank=False, max_length=65545)
    device = models.ForeignKey(Device, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['key', 'device']
