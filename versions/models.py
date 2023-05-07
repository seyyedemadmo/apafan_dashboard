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

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        super(Version, self).save(force_insert, force_update, using, update_fields)
        past_version = Version.objects.filter(company_id=self.company.id, group_id=self.group.id, type=self.type,
                                              next_version=None).exclude(id=self.id)
        if past_version:
            past_version.update(next_version=self.id)
