from django.db.models import Q
from rest_framework import serializers

from apps.hotline_ua.models import Filter
from apps.hotline_ua.serializers.category import CategorySerializer


class CreateFilterSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    code = serializers.IntegerField(required=False, allow_null=True)
    title = serializers.CharField(required=False, allow_blank=True, allow_null=True)

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
        filters = list(Filter.objects.filter(
            Q(category__path=category['path'])
        ))
        attrs['filters'] = filters if filters else []
        return attrs

    def create(self, validated_data):
        return {
            'filters': validated_data.pop('filters'),
            'category': validated_data.pop('category')
        }
