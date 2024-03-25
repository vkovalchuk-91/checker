from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Checker, Category, Filter
from apps.hotline_ua.serializers import CategorySerializer
from apps.hotline_ua.serializers.filter import FilterSerializer


class CheckerCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    filters = FilterSerializer(required=False, many=True)
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
        range_filter_dicts = []

        for filter_dict in filters:

            filter_type = FilterType.find_filter_by_value(filter_dict.get('type_name'))
            if filter_type == FilterType.TEXT:
                text_filter_dict = {**filter_dict}
                continue
            elif filter_type in [FilterType.MAX, FilterType.MIN]:
                range_filter_dicts.append({**filter_dict})
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
                {'filter': _(f'Filter "{text_filter_dict["title"]}" exist.')}
            )

        if text_filter_dict:
            attrs['text_filter'] = Filter(**text_filter_dict)

        category_instance = None
        if category.get('id'):
            category_instance = Category.objects.get(id=category['id'])
            if not category_instance.is_active or category_instance.is_link:
                raise serializers.ValidationError(
                    {'category': _(f'Invalid category id:{category["id"]} type or active state.')}
                )

        if len(filter_ids) == 0 and len(range_filter_dicts) == 0:
            if text_filter_dict:
                attrs['category'] = category_instance
                attrs['filters'] = None
                return attrs
            if not category_instance:
                raise serializers.ValidationError(
                    {'checker': _(f'Invalid empty checker.')}
                )

        attrs['category'] = category_instance
        filters = list(Filter.objects.filter(id__in=filter_ids)) if len(filter_ids) > 0 else []
        for range_filter_dict in range_filter_dicts:
            filters_instance = Filter(
                type_name=range_filter_dict['type_name'],
                code=range_filter_dict['code'],
                title=range_filter_dict['title'],
                category=category_instance,
            )
            filters.append(filters_instance)

        attrs['filters'] = filters
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

                checker = Checker(category=None, user=user, )
                checker.save()

                checker.filters.add(text_filter_instance)
                checker.updated_at = timezone.now()
                checker.save(update_fields=('updated_at',))
                checkers.append(checker)

            if category_instance:
                checker = Checker(category=category_instance, user=user, )
                checker.save()

                if filter_instances:
                    for filter_instance in filter_instances:
                        if filter_instance.type_name in [FilterType.MAX.value, FilterType.MIN.value]:
                            filter_instance.save()

                    checker.filters.set(filter_instances)
                    checker.updated_at = timezone.now()
                    checker.save(update_fields=('updated_at',))
                    checkers.append(checker)

        return checkers
