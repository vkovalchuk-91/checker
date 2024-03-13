from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.models import Category


class CategoryCreateSerializer(serializers.ModelSerializer):
    title = serializers.RegexField(
        required=True,
        regex=r'^[а-яії0-9\'. ]{2,}$',
        error_messages={'invalid': _('Invalid title.')}
    )

    class Meta:
        model = Category
        fields = (
            'title',
            'path',
        )
        extra_kwargs = {
            'title': {'required': True},
        }

    def validate(self, attrs):
        title = attrs.get('title')

        category_instances = list(Category.objects.filter(
            Q(is_active=True) & Q(is_link=False) & Q(parent_id__isnull=False) &
            (Q(title__contains=title) | Q(title__contains=title.capitalize()))
        ))

        attrs['categories'] = category_instances if category_instances else []
        return attrs

    def create(self, validated_data):
        category_instances = validated_data.pop('categories')
        return category_instances
