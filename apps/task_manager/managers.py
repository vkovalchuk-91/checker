from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from apps.accounts.models import User
from apps.common.constants import MAX_QUERY_NUMBER_DEFAULT
from apps.common.enums.checker_name import CheckerTypeName


class CheckerTaskManager(models.Manager):

    def create_task(self, checker_name: str, checker_id: str, user_id: int):
        checker_type = CheckerTypeName.find_by_value(checker_name)
        if not checker_type:
            raise ValueError('Checker type not found')

        if not self.can_create_new_checker(user_id) or self.is_exist(checker_type.value, checker_id):
            raise ValueError('Checker cannot be save.')

        checker_task = self.model(
            checker_id=checker_id,
            user_id=user_id,
            checker_type=checker_type.value,
        )

        checker_task.save(using=self._db)

        return checker_task

    def is_exist(self, checker_type, checker_id):
        return self.get_queryset().filter(
            checker_type=checker_type,
            checker_id=checker_id
        ).exists()

    def select_count(self, user_id: int) -> int:
        return self.get_queryset().filter(user_id=user_id).count()

    def select_max(self, user_pk: int) -> [int, None]:
        if not User.objects.filter(pk=user_pk).exists():
            return 0

        user = User.objects.get(pk=user_pk)
        if not user.is_active:
            return 0

        if user.is_superuser:
            return None

        if not user.personal_setting:
            return MAX_QUERY_NUMBER_DEFAULT

        if user.personal_setting.is_vip:
            return None

        return user.personal_setting.max_query_number

    def can_create_new_checker(self, user_pk: int, need_count: int = 1) -> bool:
        try:
            user = User.objects.get(pk=user_pk)
        except (MultipleObjectsReturned, User.DoesNotExist, ValueError, TypeError, OverflowError):
            return False

        if user.is_staff or user.is_superuser:
            return True

        if not user.is_active:
            return False

        max_count = self.select_max(user_pk)
        if not max_count:
            return True
        else:
            return self.select_max(user_pk) - self.select_count(user_pk) >= need_count
