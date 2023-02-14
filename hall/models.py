from django.contrib.auth import get_user_model
from django.db import models
from django.contrib.gis.db import models as g_models


class Company(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=255, help_text='company name')
    p_name = models.CharField(null=False, blank=False, max_length=255,help_text='persian company name')
    location = g_models.PolygonField(srid=4326, null=False, blank=False)
    expire_service_time = models.DateTimeField(null=True, blank=True)
    address = models.CharField(null=True, blank=True, max_length=1000)


class Hall(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=500, help_text='نام سالن')
    capacity = models.IntegerField(null=True, blank=True, help_text='ظرفیت سالن')
    geom = g_models.PolygonField(blank=False, null=False, srid=4326, help_text='موقعیت مکانی')
    created_at = models.DateTimeField(auto_now_add=True, help_text='تاریخ ساخت')
    updated_at = models.DateTimeField(auto_now=True, help_text='تاریخ آپدیت')
    company = models.ForeignKey(Company, on_delete=models.CASCADE)


class Production(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)
    capacity = models.IntegerField(null=True, blank=True)
    geom = g_models.PolygonField(srid=4326, null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, help_text='تاریخ ساخت')
    updated_at = models.DateTimeField(auto_now=True, help_text='تاریخ آپدیت')
    hall = models.ForeignKey(Hall, on_delete=models.CASCADE, null=False, blank=False)


class Group(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=500)
    capacity = models.IntegerField(null=True, blank=True)
    geom = g_models.PolygonField(blank=False, null=False, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    production = models.ForeignKey(Production, on_delete=models.CASCADE, null=False, blank=False)


class Device(g_models.Model):
    class Device_type(models.TextChoices):
        ONE_MOTOR = 'one'
        TWO_MOTOR = 'two'

    name = models.CharField(null=False, blank=False, max_length=255)
    code = models.CharField(null=False, blank=False, max_length=255)
    geom = g_models.PointField(null=False, blank=False, srid=4326)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, null=True, blank=True)
    is_connected = models.BooleanField(default=False)
    last_connected = models.DateTimeField(null=True, blank=True)
    device_type = models.CharField(choices=Device_type.choices, default=Device_type.ONE_MOTOR, max_length=255,)


class Head(g_models.Model):
    name = models.CharField(null=False, blank=False, max_length=255)
    chip_ip = models.CharField(null=False, blank=False, max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_connected = models.BooleanField(default=False)
    last_connected = models.DateTimeField(null=True, blank=True)
