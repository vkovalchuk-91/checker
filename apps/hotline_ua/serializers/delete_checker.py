from django.db import transaction

from apps.checker.serializer import BaseCheckerDeleteSerializer
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Checker
from apps.hotline_ua.models import Filter


class DeleteCheckerSerializer(BaseCheckerDeleteSerializer):
    model_class = Checker
    filter_model_class = Filter

    class Meta:
        model = Checker
        fields = [
            'id',
            'user_id',
        ]
        extra_kwargs = {
            'id': {'required': True},
            'user_id': {'required': True},
        }

    def delete(self):
        instance_id = self.validated_data['id']
        filter_instances = self.filter_model_class.objects.filter(
            checkers__id=instance_id,
            type_name__in=[FilterType.TEXT.value, FilterType.MIN_PRICE.value, FilterType.MAX_PRICE.value]
        )
        with transaction.atomic():
            for filter_instance in filter_instances:
                filter_instance.delete()
            super().delete()
