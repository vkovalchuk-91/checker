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


class SessionCheckerCounter:
    CLIENT_DATA_KEY = 'session_key'
    CLIENT_COUNTER_KEY = 'counter_key'

    def __init__(self, request):
        self.session = request.session
        client_data = request.session.get(self.CLIENT_DATA_KEY)
        if not client_data:
            self.session[self.CLIENT_DATA_KEY] = client_data = {}

        counter = client_data.get(self.CLIENT_COUNTER_KEY)

        user = request.user
        if not user.is_authenticated or not user.is_active:
            self.max_count = 0
            self.count = 0
        else:
            self.max_count = CheckerTask.objects.max_user_checkers_count(user.id)
            self.count = CheckerTask.objects.user_checkers_count(user.id)

        client_data[self.CLIENT_COUNTER_KEY] = {
            'max_count': self.max_count,
            'count': self.count,
        }

    def clear(self):
        del self.session[self.CLIENT_DATA_KEY][self.CLIENT_COUNTER_KEY]
        self.session.modified = True

    def update(self, count_value: int):
        self.count += count_value
        self.session[self.CLIENT_DATA_KEY][self.CLIENT_COUNTER_KEY]['max_count'] = self.count
        self.session.modified = True
