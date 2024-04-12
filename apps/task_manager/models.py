from django.db import models
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User, BaseParameter
from apps.common import TimeStampedMixin
from apps.common.models import ActiveStateMixin
from apps.task_manager.managers import CheckerTaskManager
from settings.main import TASK_UPDATE_PERIOD_DEFAULT, VIP_USER_TASK_UPDATE_PERIOD_DEFAULT


class CheckerTask(TimeStampedMixin, ActiveStateMixin, models.Model):
    objects = CheckerTaskManager()
    is_delete = models.BooleanField(_('delete'), default=False)
    update_period = models.IntegerField(_("update period (minutes)"), default=TASK_UPDATE_PERIOD_DEFAULT)

    task_param = models.ForeignKey(
        BaseParameter,
        on_delete=models.CASCADE,
        null=False,
        related_name='checker_task_parameters',
        verbose_name=_('checker task parameters')
    )

    user = models.ForeignKey(
        User,
        blank=False,
        on_delete=models.CASCADE,
        related_name='checker_tasks',
    )

    class Meta:
        verbose_name = _('checker_task')
        verbose_name_plural = _("checker_tasks")


class SessionTaskManager:
    CLIENT_DATA_KEY = 'session_key'
    CLIENT_COUNTER_KEY = 'counter_key'

    def __init__(self, request):
        self.session = request.session
        client_data = request.session.get(self.CLIENT_DATA_KEY)
        if not client_data:
            self.session[self.CLIENT_DATA_KEY] = client_data = {}

        counter = client_data.get(self.CLIENT_COUNTER_KEY)
        if not counter:
            counter = client_data[self.CLIENT_COUNTER_KEY] = {}

        user = request.user
        if not user.is_authenticated or not user.is_active:
            self.max_count = 0
            self.count = 0
        else:
            self.max_count = CheckerTask.objects.select_max(user.id)
            self.count = CheckerTask.objects.select_count(user.id)

        counter['max_count'] = self.max_count
        counter['user_count'] = self.count

        if user.is_superuser:
            counter['all_count'] = CheckerTask.objects.filter(is_delete=False).count()
        self.session.modified = True

    def clear(self):
        del self.session[self.CLIENT_DATA_KEY][self.CLIENT_COUNTER_KEY]
        self.session.modified = True

    def update(self, count_value: int):
        self.count += count_value
        self.session[self.CLIENT_DATA_KEY][self.CLIENT_COUNTER_KEY]['max_count'] = self.count
        self.session.modified = True
