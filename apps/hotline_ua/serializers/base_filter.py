from django.core.exceptions import MultipleObjectsReturned
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.models import Filter
from apps.hotline_ua.serializers import CategorySerializer


class BaseFilterSerializer(serializers.Serializer):
    title = serializers.RegexField(
        required=True,
        regex=r"^[a-zA-Zа-яА-ЯєіїЄІЇ0-9\-'. ]{2,100}$",
        error_messages={'invalid': _('Invalid title.')}
    )
    category = CategorySerializer(required=False)
    type_name = serializers.CharField(required=False)
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
            'type_name': {'required': False},
        }

    def validate(self, attrs):
        category = attrs.get('category')
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
                    {'filter': _(f'Invalid filter.')}
                )

        attrs['id'] = filter_instance.id
        attrs['code'] = filter_instance.code
        attrs['title'] = filter_instance.title
        attrs['type_name'] = filter_instance.type_name

        return attrs
