from django.conf import settings
from django.db import models

from rest_framework.exceptions import ValidationError

import mimetypes

from hall.models import Company, Squad


class Version(models.Model):
    class TYPE_CHOICE(models.TextChoices):
        FRAME = "frame"
        FILE_SYSTEM = "file_system"

    company = models.ForeignKey(Company, on_delete=models.CASCADE, blank=False, null=False)
    group = models.ForeignKey(Squad, on_delete=models.CASCADE, blank=False, null=False)
    type = models.CharField(choices=TYPE_CHOICE.choices, default=TYPE_CHOICE.FRAME, max_length=255, null=False,
                            blank=False)
    file = models.FileField(upload_to=getattr(settings, 'VERSION_PATH_TO_UPLOAD', None), blank=False, null=False)
    next_version = models.ForeignKey('Version', on_delete=models.SET_NULL, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
