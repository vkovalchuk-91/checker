from django.db import transaction

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import DeleteSerializer
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Checker
from apps.hotline_ua.models import Filter


class CheckerDeleteSerializer(DeleteSerializer):
    model_class = Checker
    filter_model_class = Filter
    checker_type = CheckerTypeName.HOTLINE_UA

    class Meta:
        model = Checker
        fields = [
            'id',
            'user_id',
        ]

    def delete(self):
        instance_id = self.validated_data['id']
        filter_instances = self.filter_model_class.objects.filter(
            checkers__id=instance_id,
            type_name__in=[FilterType.TEXT.value, FilterType.MIN.value, FilterType.MAX.value]
        )
        with transaction.atomic():
            for filter_instance in filter_instances:
                filter_instance.delete()
            super().delete()
