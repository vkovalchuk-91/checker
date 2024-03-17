from rest_framework import serializers

from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Filter
from apps.hotline_ua.serializers import CategorySerializer
from apps.hotline_ua.serializers.base_filter import BaseFilterSerializer
from apps.hotline_ua.serializers.range_filter import RangeFilterSerializer
from apps.hotline_ua.serializers.text_filter import TextFilterSerializer


class FilterSerializer(serializers.Serializer):
    title = serializers.CharField(required=True, )
    category = CategorySerializer(required=False)
    code = serializers.IntegerField(required=False, min_value=0, allow_null=True)
    type_name = serializers.CharField(required=False, max_length=20)

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
            # 'type_name': {'required': False},
        }

    def validate(self, attrs):
        type_name = FilterType.find_filter_by_value(attrs.get('type_name'))
        if type_name and type_name == FilterType.TEXT:
            text_serializer = TextFilterSerializer(data=attrs)
            text_serializer.is_valid(raise_exception=True)
            return text_serializer.validated_data

        if type_name and type_name in [FilterType.MAX, FilterType.MIN]:
            range_serializer = RangeFilterSerializer(data=attrs)
            range_serializer.is_valid(raise_exception=True)
            return range_serializer.validated_data

        base_serializer = BaseFilterSerializer(data=attrs)
        base_serializer.is_valid(raise_exception=True)
        return base_serializer.validated_data
