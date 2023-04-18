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
    file = models.FilePathField(path="datas/version/", blank=False, null=False)
    next_version = models.ForeignKey('Version', on_delete=models.SET_NULL, blank=True, null=True)

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        mine_type = mimetypes.guess_type(self.file)
        if not mine_type[0] == "application/octet-stream":
            ValidationError("you must enter a .bin file")
        super(Version, self).save(force_insert, force_update, using, update_fields)
