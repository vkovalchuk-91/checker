from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from apps.accounts.models import User
from apps.common.constants import MAX_QUERY_NUMBER
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

    def user_checkers_count(self, user_id: int) -> int:
        return self.get_queryset().filter(user_id=user_id).count()

    def max_user_checkers_count(self, user_pk: int) -> int:
        if not User.objects.filter(pk=user_pk).exists():
            return MAX_QUERY_NUMBER

        user = User.objects.get(pk=user_pk)
        if not user.is_active:
            return 0

        if not user.personal_setting:
            return MAX_QUERY_NUMBER

        return user.personal_setting.max_query_number

    def can_create_new_checker(self, user_pk: int) -> bool:
        try:
            user = User.objects.get(pk=user_pk)
        except (MultipleObjectsReturned, User.DoesNotExist, ValueError, TypeError, OverflowError):
            return False

        if user.is_staff or user.is_superuser:
            return True

        if not user.is_active:
            return False

        return self.user_checkers_count(user_pk) < self.max_user_checkers_count(user_pk)

    def can_create_count(self, user_pk: int) -> int:
        if not self.can_create_new_checker(user_pk):
            return 0
        return self.max_user_checkers_count(user_pk) - self.user_checkers_count(user_pk)
