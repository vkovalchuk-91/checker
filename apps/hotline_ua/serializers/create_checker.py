from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.hotline_ua.models import Checker, Category, Filter
from apps.hotline_ua.serializers import CategorySerializer
from apps.hotline_ua.serializers.filter import FilterSerializer


class CreateCheckerSerializer(serializers.ModelSerializer):
    category = CategorySerializer(required=True)
    filters = FilterSerializer(required=True, many=True)
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

        filter_ids = []
        text_filter_dict = None
        for filter_dict in filters:
            if not filter_dict['category'] and not filter_dict['id']:
                text_filter_dict = {
                    'code': -1,
                    'title': filter_dict['title'],
                    'category': None,
                    'type_name': filter_dict['type_name'],
                }
                continue
            if filter_dict['category']['id'] != category['id']:
                raise serializers.ValidationError(
                    {'filters': _(f"Filters must be from one category.")}
                )
            filter_ids.append(filter_dict['id'])

        try:
            user = attrs['user'] = User.objects.get(id=attrs['user_id'])
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid to user.')}
            )

        if text_filter_dict and Filter.objects.filter(
                title__iexact=text_filter_dict['title'],
                type_name=text_filter_dict['type_name'],
                checkers__user_id=user.id).exists():
            raise serializers.ValidationError(
                {'filter': _(f'Filter exist.')}
            )

        if not text_filter_dict and len(filter_ids) == 0:
            raise serializers.ValidationError(
                {'filter': _(f"Filters can't be empty.")}
            )

        if text_filter_dict:
            attrs['text_filter'] = Filter(**text_filter_dict)

        if len(filter_ids) == 0:
            attrs['category'] = None
            attrs['filters'] = None
            return attrs

        category_instance = Category.objects.get(id=category['id'])
        if not category_instance.is_active or category_instance.is_link:
            raise serializers.ValidationError(
                {'category': _(f'Invalid category type or active state.')}
            )

        if not text_filter_dict and len(filter_ids) == 0:
            raise serializers.ValidationError(
                {'filter': _(f"Filters can't be empty.")}
            )

        attrs['category'] = category_instance
        attrs['filters'] = Filter.objects.filter(id__in=filter_ids) if len(filter_ids) > 0 else []

        return attrs

    def create(self, validated_data):
        text_filter_instance = validated_data.get('text_filter')
        filter_instances = validated_data['filters']
        category_instance = validated_data['category']
        user = validated_data['user']

        checkers = []
        with transaction.atomic():
            if text_filter_instance:
                text_filter_instance.save()
                checker = Checker(
                    category=None,
                    user=user,
                )
                checker.save()
                checker.filters.add(text_filter_instance)
                checker.updated_at = timezone.now()
                checker.save(update_fields=('updated_at',))
                checkers.append(checker)

            if filter_instances:
                checker = Checker(
                    category=category_instance,
                    user=user,
                )
                checker.save()
                checker.filters.set(filter_instances)
                checker.updated_at = timezone.now()
                checker.save(update_fields=('updated_at',))
                checkers.append(checker)

        return checkers
