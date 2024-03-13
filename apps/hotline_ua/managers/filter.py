from django.db import models, transaction
from django.utils import timezone


class FilterManager(models.Manager):

    def save_all(self, filter_instances):
        if not filter_instances:
            raise ValueError('No filters instances provided.')

        if len(filter_instances) == 0:
            return filter_instances

        with transaction.atomic():
            for filter_instance in filter_instances:
                filter_instance.save()
            return filter_instances

    def get_instance(self, instance_dict: dict):
        queryset = super().get_queryset()

        if queryset.filter(code=instance_dict['code']).exists():
            instance = queryset.get(code=instance_dict['code'])
            instance.updated_at = timezone.now()
        else:
            instance = self.model()

        instance.code = instance_dict['code']
        instance.title = instance_dict['title']
        instance.type_name = instance_dict['type_name']

        return instance
