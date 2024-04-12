from django.core.exceptions import MultipleObjectsReturned
from django.db import models

from apps.accounts.models import User
from settings.main import MAX_QUERY_NUMBER_DEFAULT


class CheckerTaskManager(models.Manager):
    def select_count(self, user_id: int) -> int:
        return self.get_queryset().filter(
            user_id=user_id,
            is_delete=False,
        ).count()

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

    def can_create_new_task(self, user_pk: int, need_count: int = 1) -> bool:
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
