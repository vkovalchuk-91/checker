from django.db import transaction
from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseDeleteSerializer
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import BaseSearchParameter
from apps.hotline_ua.models import Filter


class CheckerDeleteSerializer(BaseDeleteSerializer, serializers.ModelSerializer):
    model_class = BaseSearchParameter
    filter_model_class = Filter
    checker_type = CheckerTypeName.HOTLINE_UA

    class Meta:
        model = BaseSearchParameter
        fields = [
            'id',
            'user_id',
        ]

    def delete(self):
        instance = self.validated_data['instance']
        task_instance = self.validated_data['task_instance']
        filter_instances = self.filter_model_class.objects.filter(
            search_parameters__id=instance.id,
            type_name__in=[FilterType.TEXT.value, FilterType.MIN.value, FilterType.MAX.value, FilterType.LINK.value]
        )
        with transaction.atomic():
            for filter_instance in filter_instances:
                filter_instance.delete()
            instance.filters.clear()
            instance.delete()
            task_instance.task_param.delete()
            task_instance.delete()
