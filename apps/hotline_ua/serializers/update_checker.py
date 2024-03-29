from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseUpdateSerializer
from apps.hotline_ua.models import BaseSearchParameter


class CheckerUpdateSerializer(BaseUpdateSerializer, serializers.ModelSerializer):
    model_class = BaseSearchParameter
    checker_type = CheckerTypeName.HOTLINE_UA

    class Meta:
        model = BaseSearchParameter
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
