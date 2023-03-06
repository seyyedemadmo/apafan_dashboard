import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
from hall.models import Company


class User(AbstractUser):
    is_admin = models.BooleanField(default=False)
    is_band = models.BooleanField(default=False)
    company = models.ForeignKey(Company, on_delete=models.PROTECT, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expire_time = models.DateTimeField(null=True, blank=True)
    uuid = models.CharField(unique=True, null=True, blank=True, max_length=50)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def save(self, *args, **kwargs):
        if self.company:
            self.is_admin = True
        if not self.uuid:
            self.uuid = uuid.uuid4().__str__()
        super(User, self).save(*args, **kwargs)
