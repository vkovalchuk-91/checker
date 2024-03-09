from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.tickets_ua.managers import CheckerManager
from apps.common import TimeStampedMixin


class Station(models.Model):
    title = models.CharField(_('title'), max_length=100, blank=False)
    value = models.IntegerField(_('value'), unique=True)

    def __str__(self):
        return self.title


class Checker(TimeStampedMixin, models.Model):
    objects = CheckerManager()

    from_station = models.ForeignKey(
        'Station',
        blank=False,
        on_delete=models.CASCADE,
        related_name='from_station_checkers'
    )

    to_station = models.ForeignKey(
        'Station',
        blank=False,
        on_delete=models.CASCADE,
        related_name='to_station_checkers'
    )

    date_at = models.DateField(_('at date'), default=timezone.now)
    time_at = models.TimeField(_('at time'), default=timezone.now)

    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='users',
    )

    is_active = models.BooleanField(_('active'), default=True)
    is_available = models.BooleanField(_('available'), default=False)

    class Meta:
        verbose_name = _("checker")
        verbose_name_plural = _("checkers")

    def __str__(self):
        return f'{self.from_station}-{self.to_station}'
