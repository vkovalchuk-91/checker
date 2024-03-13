from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class BaseFilterChoices(models.TextChoices):
    DEFAULT = 'default', _('default')


class BaseFilter(models.Model):
    type_choices_class = BaseFilterChoices

    type_name = models.CharField(
        _('type'),
        max_length=20,
        blank=False,
        choices=type_choices_class.choices,
    )

    class Meta:
        abstract = True


class BaseChecker(models.Model):
    filter_class = None

    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='checkers',
    )

    is_active = models.BooleanField(_('active'), default=True)
    is_available = models.BooleanField(_('available'), default=False)

    class Meta:
        abstract = True
