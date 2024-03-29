from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User, BaseParameter
from apps.common import TimeStampedMixin
from apps.common.models import ActiveStateMixin, AvailableStateMixin
from apps.tickets_ua.managers import BaseParameterManager


class Station(models.Model):
    code = models.IntegerField(_('code'), unique=True)
    name = models.CharField(_('title'), max_length=100, blank=False)
    bus_name = models.CharField(_('bus name'), max_length=100, blank=True, default='')

    def __str__(self):
        return self.name


class BaseSearchParameter(TimeStampedMixin, ActiveStateMixin, AvailableStateMixin, models.Model):
    objects = BaseParameterManager()

    param_type = models.OneToOneField(
        BaseParameter,
        parent_link=True,
        on_delete=models.CASCADE,
        related_name='ticket_ua_search_parameters'
    )

    from_station = models.ForeignKey(
        'Station',
        blank=False,
        on_delete=models.CASCADE,
        related_name='from_station_parameters'
    )

    to_station = models.ForeignKey(
        'Station',
        blank=False,
        on_delete=models.CASCADE,
        related_name='to_station_parameters'
    )

    date_at = models.DateField(_('at date'), default=timezone.now)
    time_at = models.TimeField(_('at time'), default=timezone.now)

    class Meta:
        verbose_name = _("search_parameters")
        verbose_name_plural = _("search parameters")

    def __str__(self):
        return f'{self.from_station}-{self.to_station}'
