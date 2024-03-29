from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseDeleteSerializer
from apps.tickets_ua.models import BaseSearchParameter


class CheckerDeleteSerializer(BaseDeleteSerializer, serializers.ModelSerializer):
    model_class = BaseSearchParameter
    checker_type = CheckerTypeName.TICKETS_UA

    class Meta:
        model = BaseSearchParameter
        fields = [
            'id',
            'user_id',
        ]
