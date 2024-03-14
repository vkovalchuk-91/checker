from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.hotline_ua.models import Checker, Category, Filter
from apps.hotline_ua.serializers import CategorySerializer
from apps.hotline_ua.serializers.filter import FilterSerializer


class CreateCheckerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    filters = FilterSerializer(many=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Checker
        fields = [
            'id',
            'filters',
            'category',
            'user_id',
        ]

    def validate(self, attrs):
        filters = attrs['filters']
        category = attrs['category']

        for filter_dict in filters:
            if filter_dict['category']['id'] != category['id']:
                raise serializers.ValidationError(
                    {'filters': _(f'Invalid filters.')}
                )

        try:
            attrs['user'] = User.objects.get(id=attrs['user_id'])
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid to user.')}
            )

        category_instance = Category.objects.get(id == category['id'])
        if not category_instance.is_active or category_instance.is_link:
            raise serializers.ValidationError(
                {'category': _(f'Invalid category.')}
            )

        attrs['category'] = category_instance
        attrs['filters'] = Filter.objects.filter(id__in=[filter_dict['id'] for filter_dict in filters])

        return attrs

    def create(self, validated_data):
        checker = Checker(
            category=validated_data['category'],
            filters=validated_data['filters'],
        )
        checker.save()

        return checker
