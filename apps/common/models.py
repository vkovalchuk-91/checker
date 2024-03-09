from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _


class TimeStampedMixin(models.Model):
    created_at = models.DateTimeField(_('created date'), default=timezone.now)
    updated_at = models.DateTimeField(_('updated date'), default=timezone.now)

    class Meta:
        abstract = True
