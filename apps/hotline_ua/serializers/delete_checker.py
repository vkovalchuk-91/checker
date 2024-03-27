from django.db import transaction
from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseDeleteSerializer
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Checker
from apps.hotline_ua.models import Filter


class CheckerDeleteSerializer(BaseDeleteSerializer, serializers.ModelSerializer):
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
        checker_instance = self.validated_data['checker']
        filter_instances = self.filter_model_class.objects.filter(
            checkers__id=checker_instance.id,
            type_name__in=[FilterType.TEXT.value, FilterType.MIN.value, FilterType.MAX.value]
        )
        with transaction.atomic():
            checker_instance.filters.clear()
            for filter_instance in filter_instances:
                filter_instance.delete()
            super().delete()
