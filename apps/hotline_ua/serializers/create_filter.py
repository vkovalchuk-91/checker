from rest_framework import serializers

from apps.common.constants import DEFAULT_TITLE_REGEX
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Filter, Category
from apps.hotline_ua.serializers.base_category import CategorySerializer
from apps.hotline_ua.tasks import scraping_categories_filters


class FilterCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    code = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.RegexField(
        required=False,
        regex=DEFAULT_TITLE_REGEX,
        allow_blank=True,
        allow_null=True)

    class Meta:
        model = Filter
        fields = (
            'code',
            'title',
            'type_name',
            'category',
        )
        extra_kwargs = {
            'type_name': {'required': False},
        }

    def validate(self, attrs):
        category_id = attrs['category']['id']

        filters = self._get_link_filters(category_id)

        filters.extend(Filter.objects.filter(
            category_id=category_id,
            type_name__in=[FilterType.BRAND.value, FilterType.SHOP.value]
        ))
        if not filters or len(filters) == 0:
            scraping_categories_filters([category_id])
            filters = Filter.objects.filter(category_id=category_id, )

        attrs['filters'] = filters if filters else []
        return attrs

    def _get_link_filters(self, category_id: int) -> list:
        category = Category.objects.get(id=category_id)
        link_categories = Category.objects.filter(
            is_active=True,
            is_link=True,
            parent_id=category.parent_id,
            url__istartswith=category.url,
            path__regex=r'^[0-9-]+$',
        )

        link_filters = []
        codes = []
        for instance in link_categories:
            for code in instance.path.split("-"):
                if code not in codes:
                    codes.append(code)
                    link_filters.append(
                        Filter(
                            code=code,
                            title=instance.title,
                            type_name=FilterType.LINK.value,
                            category=category,
                        )
                    )

        return link_filters

    def create(self, validated_data):
        return validated_data['filters']
