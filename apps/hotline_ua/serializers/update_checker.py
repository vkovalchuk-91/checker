from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseUpdateSerializer
from apps.hotline_ua.models import Checker


class CheckerUpdateSerializer(BaseUpdateSerializer, serializers.ModelSerializer):
    model_class = Checker
    checker_type = CheckerTypeName.HOTLINE_UA

    class Meta:
        model = Checker
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
