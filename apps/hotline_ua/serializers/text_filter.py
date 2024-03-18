from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Filter


class TextFilterSerializer(serializers.Serializer):
    type_name = serializers.CharField(required=True, max_length=20)
    title = serializers.RegexField(
        required=True,
        regex=r"^[a-zA-Zа-яА-ЯєіїЄІЇ0-9\-'. ]{2,100}$",
        error_messages={'invalid': _('Invalid title.')}
    )
    category = serializers.CharField(read_only=True, required=False)

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
        type_name = FilterType.find_filter_by_value(attrs.get('type_name'))
        if not type_name:
            raise serializers.ValidationError(
                {'type_name': _(f'Invalid type name.')}
            )

        if type_name != FilterType.TEXT:
            raise serializers.ValidationError(
                {'type_name': _(f'Not text filter type.')}
            )

        attrs['id'] = None
        attrs['code'] = -1
        attrs['title'] = attrs['title']
        attrs['category'] = None
        attrs['type_name'] = type_name.value
        return attrs
