from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.common.constants import TITLE_REGEX_DEFAULT
from apps.hotline_ua.models import Category
from apps.hotline_ua.tasks import scraping_categories


class CategorySerializer(serializers.Serializer):
    title = serializers.RegexField(
        required=True,
        regex=TITLE_REGEX_DEFAULT,
        error_messages={'invalid': _('Invalid title.')},
        allow_blank=True,
    )
    path = serializers.CharField(required=False, max_length=100)

    class Meta:
        model = Category
        fields = [
            'id',
            'title',
            'path',
            'is_link',
        ]
        extra_kwargs = {
            'id': {'required': False},
            'is_link': {'required': False},
        }

    def validate(self, attrs):
        if attrs.get('title') == '' and attrs.get('path') is None:
            return attrs

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
                scraping_categories()
                category = Category.objects.get(
                    title__iexact=attrs['title'],
                    is_active=True,
                    is_link=False,
                    parent__isnull=False
                )
            except (Category.DoesNotExist, ValueError, TypeError, OverflowError):
                raise serializers.ValidationError(
                    {'category': _(f'Invalid category.')}
                )

        attrs['is_link'] = category.is_link
        attrs['title'] = category.title
        attrs['path'] = category.path
        attrs['id'] = category.id

        return attrs
