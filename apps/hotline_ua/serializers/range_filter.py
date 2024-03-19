from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.serializers import CategorySerializer


class RangeFilterSerializer(serializers.Serializer):
    type_name = serializers.CharField(required=True, max_length=20)
    code = serializers.IntegerField(required=True, min_value=0)
    category = CategorySerializer(required=True)

    def validate(self, attrs):
        type_name = FilterType.find_filter_by_value(attrs.get('type_name'))
        if not type_name:
            raise serializers.ValidationError(
                {'type_name': _(f'Invalid type name.')}
            )

        if type_name not in [FilterType.MAX, FilterType.MIN]:
            raise serializers.ValidationError(
                {'type_name': _(f'Not range filter type.')}
            )

        category = attrs['category']
        if not category or not category.get('id'):
            raise serializers.ValidationError(
                {'category': _(f'Invalid category.')}
            )

        attrs['id'] = None
        attrs['code'] = attrs['code']
        attrs['title'] = type_name.value
        attrs['type_name'] = type_name.value
        return attrs
