from django.db import models

from hall.models import Head, Device


class HeadData(models.Model):
    chip_id = models.CharField(null=False, blank=False, max_length=255)
    receive_at = models.DateTimeField(auto_now_add=True)
    device = models.ForeignKey(Device, on_delete=models.DO_NOTHING)
    data = models.JSONField(blank=True, null=True)


class TempDevice(models.Model):
    chip_id = models.CharField(null=False, blank=False, max_length=500)
    mac_address = models.CharField(null=False, blank=False, max_length=500)
    ready = models.BooleanField(default=False)
