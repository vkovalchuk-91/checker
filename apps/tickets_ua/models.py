from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.common import TimeStampedMixin
from apps.common.models import StateMixin
from apps.tickets_ua.managers import CheckerManager


class Station(models.Model):
    code = models.IntegerField(_('code'), unique=True)
    name = models.CharField(_('title'), max_length=100, blank=False)
    bus_name = models.CharField(_('bus name'), max_length=100, blank=True, default='')

    def __str__(self):
        return self.name


class Checker(TimeStampedMixin, StateMixin, models.Model):
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
        related_name='tickets_ua_checkers',
    )

    class Meta:
        verbose_name = _("checker")
        verbose_name_plural = _("checkers")

    def __str__(self):
        return f'{self.from_station}-{self.to_station}'
