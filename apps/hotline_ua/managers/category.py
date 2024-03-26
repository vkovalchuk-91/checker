from django.db import models, transaction
from django.utils import timezone


class CategoryManager(models.Manager):
    DEFAULT_ACTIVE_TITLE_CATEGORIES = ["Побутова техніка", "Комп'ютери", "Смартфони"]

    def save_with_children(self, instance_dict):
        instance = self.get_instance(instance_dict)
        instance.is_active = self.default_active_state(instance)

        if not instance_dict.get('children'):
            instance.save()
            return instance

        children_instance = []
        for child in instance_dict['children']:
            child_dict = child.__dict__
            child_dict['is_active'] = instance.is_active
            children_instance.append(self.get_instance(child_dict))

        with transaction.atomic():
            instance.save()
            instances = [instance]
            for child_instance in children_instance:
                child_instance.parent = instance
                child_instance.save()
                instances.append(child_instance)

        return instances

    def default_active_state(self, instance):
        for title in self.DEFAULT_ACTIVE_TITLE_CATEGORIES:
            if title.lower() in instance.title.lower():
                return True

        return False

    def get_instance(self, instance_dict):
        queryset = self.get_queryset()

        if queryset.filter(code=instance_dict['code']).exists():
            instance = queryset.get(code=instance_dict['code'])
            instance.updated_at = timezone.now()
        else:
            instance = self.model()

        instance.code = instance_dict['code']
        instance.title = instance_dict['title']
        instance.url = instance_dict['url']
        instance.path = instance_dict['path']
        instance.is_link = instance_dict['is_link']
        instance.is_active = instance_dict['is_active'] if instance_dict.get('is_active') else False

        return instance
