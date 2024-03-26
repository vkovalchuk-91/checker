from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User
from apps.common import TimeStampedMixin
from apps.common.constants import TASK_UPDATE_PERIOD_DEFAULT
from apps.common.models import ActiveStateMixin
from apps.common.enums.checker_name import CheckerTypeName
from apps.task_manager.managers import CheckerTaskManager


class CheckerTypeNameChoices(models.TextChoices):
    HOTLINE_UA = CheckerTypeName.HOTLINE_UA.value
    TICKETS_UA = CheckerTypeName.TICKETS_UA.value


class CheckerTask(TimeStampedMixin, ActiveStateMixin, models.Model):
    objects = CheckerTaskManager()

    checker_id = models.IntegerField(_("checker id"))
    update_period = models.IntegerField(_("update period (minutes)"), default=TASK_UPDATE_PERIOD_DEFAULT)

    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='checker_tasks',
    )

    checker_type = models.CharField(
        _('checker type name'),
        max_length=20,
        choices=CheckerTypeNameChoices.choices,
    )

    class Meta:
        unique_together = ('checker_type', 'checker_id')
        verbose_name = _("checker_task")
        verbose_name_plural = _("checker_tasks")

