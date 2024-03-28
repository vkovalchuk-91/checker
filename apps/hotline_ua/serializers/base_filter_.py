from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.common.constants import DEFAULT_TITLE_REGEX
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Filter, Category
from apps.hotline_ua.serializers.base_category import CategorySerializer


class FilterInstanceSerializer(serializers.ModelSerializer):
    title = serializers.RegexField(
        required=True,
        regex=DEFAULT_TITLE_REGEX,
        error_messages={'invalid': _('Invalid title.')}
    )
    category = CategorySerializer(required=True)
    type_name = serializers.CharField(required=True)
    code = serializers.IntegerField(required=False, allow_null=True)

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
        }

    def validate(self, attrs):
        type_name = FilterType.find_by_value(attrs.get('type_name'))
        if not type_name:
            raise serializers.ValidationError(
                {'type_name': _(f'Invalid type name.')}
            )

        if type_name == FilterType.TEXT:
            instance = self._get_text_filter_instance(attrs)
        elif type_name in (FilterType.MAX, FilterType.MIN,):
            instance = self._get_range_filter_instance(attrs, type_name.value)
        elif type_name == FilterType.LINK:
            instance = self._get_link_filter_instance(attrs)
        else:
            instance = self._get_other_filter_instance(attrs)

        attrs['instance'] = instance

        return attrs

    def _get_text_filter_instance(self, attrs):
        return Filter(
            code=-1,
            title=attrs['title'],
            type_name=FilterType.TEXT.value,
            category=None,
        )

    def _get_range_filter_instance(self, attrs, type_name):
        category = attrs['category']
        if not category or not category.get('id'):
            raise serializers.ValidationError(
                {'category': _(f'Invalid category.')}
            )

        try:
            code = int(attrs['code'])
            if code < 0:
                raise ValueError
        except (ValueError, TypeError):
            raise serializers.ValidationError(
                {'code': _(f'Invalid code.')}
            )

        return Filter(
            code=code,
            title=type_name,
            type_name=type_name,
            category_id=category['id'],
        )

    def _get_link_filter_instance(self, attrs):
        category = attrs['category']
        try:
            category_instance = Category.objects.get(id=category['id'])
        except (Category.DoesNotExist, ValueError, TypeError, OverflowError, KeyError):
            raise serializers.ValidationError(
                {'category': _(f'Invalid category.')}
            )

        if not Category.objects.filter(
                is_active=True,
                is_link=True,
                parent_id=category_instance.parent_id,
                url__istartswith=category_instance.url,
                path__contains=attrs['code'],
        ).exists():
            raise serializers.ValidationError(
                {'filter': _(f'Invalid link filter:{attrs["title"]}.')}
            )

        return Filter(
            code=attrs['code'],
            title=attrs['title'],
            type_name=FilterType.LINK.value,
            category_id=category['id'],
        )

    def _get_other_filter_instance(self, attrs):
        category = attrs['category']
        if not category or not category.get('id'):
            raise serializers.ValidationError(
                {'category': _(f'Invalid category.')}
            )

        filter_instance = Filter.objects.filter(code=attrs['code'], category_id=category['id'], ).first()
        if not filter_instance:
            try:
                filter_instance = Filter.objects.get(
                    title__iexact=attrs['title'],
                    category_id=category['id'],
                )
            except (Filter.DoesNotExist, MultipleObjectsReturned, ValueError, TypeError, OverflowError):
                raise serializers.ValidationError(
                    {'filter': _(f'Invalid filter:{attrs["title"]}.')}
                )

        return filter_instance
