from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.booking_uz_gov_ua.managers import CheckerManager
from apps.common import TimeStampedMixin


class Station(models.Model):
    title = models.CharField(_('title'), max_length=100, blank=False)
    value = models.IntegerField(_('value'), unique=True)

    def __str__(self):
        return self.title


class Place(models.Model):
    letter = models.CharField(_('letter'), max_length=3)
    title = models.CharField(_('title'), max_length=100)
    places = models.IntegerField(_('free places'), default=0, blank=False)

    def __str__(self):
        return self.title


class Train(models.Model):
    num = models.CharField(_('number'), max_length=20, blank=False)
    category = models.IntegerField(_('category'), blank=True, )

    date_at = models.DateField(_('at date'), default=timezone.now)
    time_at = models.TimeField(_('at time'), default=timezone.now)

    places = models.ManyToManyField(
        'Place',
        related_name='trains',
    )

    def __str__(self):
        return self.num


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

    trains = models.ManyToManyField(
        'Train',
        blank=True,
        related_name='checkers',
    )

    class Meta:
        verbose_name = _("checker")
        verbose_name_plural = _("checkers")

    def __str__(self):
        return f'{self.from_station}-{self.to_station}'
