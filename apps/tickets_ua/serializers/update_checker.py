from rest_framework import serializers

from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import BaseUpdateSerializer
from apps.tickets_ua.models import BaseSearchParameter


class TicketsUaCheckerUpdateSerializer(BaseUpdateSerializer, serializers.ModelSerializer):
    model_class = BaseSearchParameter
    checker_type = CheckerTypeName.TICKETS_UA

    class Meta:
        model = BaseSearchParameter
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
