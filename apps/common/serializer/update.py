from django.utils import timezone
from drf_spectacular.utils import extend_schema_serializer, OpenApiExample
from rest_framework import serializers

from apps.common.serializer.base import BaseSerializer


@extend_schema_serializer(
    examples=[
        OpenApiExample(
            'Request Value',
            value={
                'is_active': 'true'
            },
            request_only=True,
            response_only=False,
        ),
        OpenApiExample(
            'Response Value',
            value={
                'id': 0,
                'is_active': 'true'
            },
            request_only=False,
            response_only=False,
        ),
    ]
)
class BaseUpdateSerializer(BaseSerializer, serializers.Serializer):
    is_active = serializers.BooleanField(required=True)

    class Meta:
        abstract = True

    def create(self, validated_data):
        instance = self.validated_data['instance']
        is_active = self.validated_data['is_active']
        instance.is_active = is_active
        instance.updated_at = timezone.now()
        instance.save(update_fields=('is_active', 'updated_at',))
        return instance
