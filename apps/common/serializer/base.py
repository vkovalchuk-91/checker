from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.task_manager.models import CheckerTask


class BaseSerializer(serializers.Serializer):
    model_class = None
    checker_type = None
    user_model_class = User
    checker_task_model_class = CheckerTask

    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        abstract = True

    def validate(self, attrs):
        try:
            checker_instance = self.model_class.objects.get(id=attrs['id'])
        except (self.model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'id': _(f'Invalid identification checker by id:{id}.')}
            )

        try:
            checker_task_instance = self.checker_task_model_class.objects.get(
                checker_id=attrs['id'],
                checker_type=self.checker_type.value
            )
        except (self.checker_task_model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'checker': _(f'Invalid identification checker task.')}
            )

        try:
            user = self.user_model_class.objects.get(id=attrs['user_id'])
            if checker_task_instance.user.id != user.id and not user.is_superuser:
                raise ValueError
        except (self.user_model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid identification user or permissions.')}
            )

        attrs['checker'] = checker_instance
        attrs['checker_task'] = checker_task_instance

        return attrs
