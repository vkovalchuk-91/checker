import re

from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.models import Category

DATA_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class CategorySerializer(serializers.Serializer):
    title = serializers.CharField(required=True, min_length=2, max_length=100)
    path = serializers.CharField(required=True, max_length=100)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'path',
        ]
        extra_kwargs = {
            'id': {'required': False}
        }

    def validate(self, attrs):
        title = attrs['title']

        pattern = re.compile(r'^[a-zа-яії0-9\'. ]+$')
        if not bool(pattern.match(title.lower())):
            raise serializers.ValidationError(
                {'title': _(f'Invalid title.')}
            )

        try:
            category = Category.objects.get(
                path__iexact=attrs['path'],
                is_active=True,
                is_link=False,
                parent__isnull=False
            )
        except MultipleObjectsReturned:
            category = Category.objects.filter(
                path__iexact=attrs['path'],
                is_active=True,
                is_link=False,
                parent__isnull=False
            )[0]
        except (Category.DoesNotExist, ValueError, TypeError, OverflowError):
            try:
                category = Category.objects.get(
                    title__iexact=attrs['title'],
                    is_active=True,
                    is_link=False,
                    parent__isnull=False
                )
            except (Category.DoesNotExist, ValueError, TypeError, OverflowError):
                return attrs

        attrs['title'] = category.title
        attrs['path'] = category.path
        attrs['id'] = category.id

        return attrs
