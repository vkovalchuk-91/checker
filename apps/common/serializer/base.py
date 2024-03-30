from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import BaseParameter
from apps.accounts.models import User
from apps.common.enums.checker_name import CheckerTypeName
from apps.task_manager.models import CheckerTask


class BaseSerializer(serializers.Serializer):
    model_class = None
    checker_type = None
    user_model_class = User

    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        abstract = True

    def validate(self, attrs):
        try:
            instance = self.model_class.objects.get(id=attrs['id'])
        except (self.model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'parameters': _(f'Invalid identification parameters by id:{id}.')}
            )

        try:
            base_param = BaseParameter.objects.get(id=instance.param_type.param_type_id)
        except (BaseParameter.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'base_param': _(f'Invalid identification base parameter.')}
            )

        category_name = base_param.param_type.param_category_name
        type_name = CheckerTypeName.find_by_value(category_name)

        try:
            if type_name == CheckerTypeName.HOTLINE_UA:
                task_instance = CheckerTask.objects.get(task_param__hotline_ua_search_parameters__id=attrs['id'])
            elif type_name == CheckerTypeName.TICKETS_UA:
                task_instance = CheckerTask.objects.get(task_param__ticket_ua_search_parameters__id=attrs['id'])
            else:
                raise ValueError
        except (CheckerTask.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'task': _(f'Invalid identification checker task.')}
            )

        try:
            user = self.user_model_class.objects.get(id=attrs['user_id'])
            if task_instance.user.id != user.id and not user.is_superuser:
                raise ValueError
        except (self.user_model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid identification user or permissions.')}
            )

        attrs['instance'] = instance
        attrs['task_instance'] = task_instance

        return attrs
