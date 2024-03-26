from django.db import transaction
from rest_framework import serializers

from apps.common.serializer.base import BaseSerializer


class DeleteSerializer(BaseSerializer, serializers.ModelSerializer):
    class Meta:
        abstract = True

    def delete(self):
        checker_instance = self.validated_data['checker']
        checker_task_instance = self.validated_data['checker_task']
        with transaction.atomic():
            checker_instance.delete()
            checker_task_instance.delete()