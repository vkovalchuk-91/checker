from django.db import transaction
from rest_framework import serializers

from apps.common.serializer.base import BaseSerializer


class BaseDeleteSerializer(BaseSerializer, serializers.Serializer):
    class Meta:
        abstract = True

    def delete(self):
        instance = self.validated_data['instance']
        task_instance = self.validated_data['task_instance']
        with transaction.atomic():
            instance.delete()
            task_instance.task_param.delete()
            task_instance.delete()
