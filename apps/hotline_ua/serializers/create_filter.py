from rest_framework import serializers

from apps.hotline_ua.models import Filter
from apps.hotline_ua.serializers.category import CategorySerializer
from apps.hotline_ua.tasks import scraping_categories_filters


class FilterCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    code = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.RegexField(
        required=False,
        regex=r"^[a-zA-Zа-яА-ЯєіїЄІЇ0-9\-'. ]{2,100}$",
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
            'code': {'required': False},
            'title': {'required': False},
            'type_name': {'required': False},
            # 'category': {'required': True},
        }

    def validate(self, attrs):
        category = attrs.get('category')
        filters = Filter.objects.filter(category__path=category['path'])
        if not filters or len(filters) == 0:
            scraping_categories_filters([category['id']])
            filters = Filter.objects.filter(category__path=category['path'])

        attrs['filters'] = filters if filters else []
        return attrs

    def create(self, validated_data):
        return validated_data['filters']
