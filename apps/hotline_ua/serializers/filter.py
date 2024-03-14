import re

from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.models import Filter
from apps.hotline_ua.serializers import CategorySerializer


class FilterSerializer(serializers.Serializer):
    category = CategorySerializer(required=True)
    title = serializers.CharField(required=True, min_length=2, max_length=100, )
    code = serializers.IntegerField(required=False, )

    class Meta:
        model = Filter
        fields = [
            'id',
            'code',
            'title',
            'type_name',
            'category',
        ]
        extra_kwargs = {
            'id': {'required': False},
            'type_name': {'required': False},
        }

    def validate(self, attrs):
        title = attrs['title']

        pattern = re.compile(r'^[a-zа-яії0-9\'. ]+$')
        if not bool(pattern.match(title.lower())):
            raise serializers.ValidationError(
                {'title': _(f'Invalid title.')}
            )

        category = attrs['category']
        try:
            filter_instance = Filter.objects.get(
                code=attrs['code'],
                category_id=category['id'],
            )
        except MultipleObjectsReturned:
            filter_instance = Filter.objects.filter(
                codet=attrs['code'],
                category_id=category['id'],
            )[0]
        except (Filter.DoesNotExist, ValueError, TypeError, OverflowError):
            try:
                filter_instance = Filter.objects.get(
                    title__iexact=attrs['title'],
                    category_id=category['id'],
                )
            except (Filter.DoesNotExist, MultipleObjectsReturned, ValueError, TypeError, OverflowError):
                raise serializers.ValidationError(
                    {'title': _(f'Invalid title.')}
                )

        attrs['id'] = filter_instance.id
        attrs['code'] = filter_instance.code
        attrs['title'] = filter_instance.title
        attrs['type_name'] = filter_instance.type_name

        return attrs
