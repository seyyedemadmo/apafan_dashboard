from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db import models as g_models


class Company(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text='company name')
    p_name = models.CharField(null=False, blank=False, max_length=255, help_text='persian company name')
    location = g_models.PolygonField(srid=4326, null=False, blank=False)
    expire_service_time = models.DateTimeField(null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=1000)

    def __str__(self):
        return self.name


class Squad(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=500)
    capacity = models.IntegerField(null=True, blank=True)
    geom = g_models.PolygonField(blank=False, null=False, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=False, blank=False)

    def __str__(self):
        return self.name


class DeviceType(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=225)
    company = models.ManyToManyField(Company)

    def __str__(self):
        return self.name


class Device(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)
    code = models.CharField(null=False, blank=False, max_length=255)
    chip_ip = models.CharField(null=False, blank=False, unique=True, max_length=255)
    geom = g_models.PointField(null=False, blank=False, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Squad, on_delete=models.SET_NULL, null=True, blank=True)
    is_connected = models.BooleanField(default=False)
    last_connected = models.DateTimeField(null=True, blank=True)
    device_type = models.ForeignKey(DeviceType, on_delete=models.CASCADE, null=False, blank=False)
    status = models.BinaryField(blank=True, null=True)
    command = models.BinaryField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if (self.status and len(self.status) > 4) or (self.command and len(self.command) > 4):
            raise ValueError("The binary fields cannot be longer than 32 bits (4 bytes).")
        super().save(*args, **kwargs)




