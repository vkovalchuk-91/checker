from django.utils import timezone
from rest_framework import serializers

from apps.common.serializer.base import BaseSerializer


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
