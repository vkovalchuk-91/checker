from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import Checker, Category, Filter
from apps.hotline_ua.serializers import CategorySerializer
from apps.hotline_ua.serializers.filter import FilterSerializer
from apps.common.enums.checker_name import CheckerTypeName
from apps.task_manager.models import CheckerTask


class CheckerCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    filters = FilterSerializer(required=False, many=True)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = Checker
        fields = [
            'id',
            'filters',
            'category',
            'user_id',
        ]

    def validate(self, attrs):
        if not attrs.get('user_id'):
            raise serializers.ValidationError(
                {'user': _(f'Invalid identification user.')}
            )

        can_create_count = CheckerTask.objects.can_create_count(attrs['user_id'])
        if can_create_count == 0:
            raise serializers.ValidationError(
                {'checker': _(f"Can't create a new checker.")}
            )

        category = attrs['category']
        filters = self._get_filter_dict_by_type(attrs)
        text_filter_dict = filters["text_filter"]
        range_filter_dicts = filters["range_filter"]
        filter_ids = filters['filter_ids']

        category_instance = None
        if category.get('id'):
            category_instance = Category.objects.get(id=category['id'])
            if not category_instance.is_active or category_instance.is_link:
                raise serializers.ValidationError(
                    {'category': _(f'Invalid category id:{category["id"]} type or active state.')}
                )

        if category_instance and text_filter_dict and can_create_count < 2:
            raise serializers.ValidationError(
                {'checker': _(f'Cannot create more then 1 checker.')}
            )

        if text_filter_dict:
            attrs['text_filter'] = Filter(**text_filter_dict)

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

    def _get_filter_dict_by_type(self, attrs):
        filter_ids = []
        text_filter_dict = None
        range_filter_dicts = []
        for filter_dict in attrs['filters']:

            filter_type = FilterType.find_by_value(filter_dict.get('type_name'))
            if filter_type == FilterType.TEXT:
                text_filter_dict = {**filter_dict, 'category': None}
                continue
            elif filter_type in [FilterType.MAX, FilterType.MIN]:
                range_filter_dicts.append({**filter_dict})
                continue

            if filter_dict['category']['id'] != attrs['category']['id']:
                raise serializers.ValidationError(
                    {'filters': _(f"Filters must be from one category.")}
                )

            filter_ids.append(filter_dict['id'])

        return {
            'text_filter': text_filter_dict,
            'range_filter': range_filter_dicts,
            'filter_ids': filter_ids,
        }

    def create(self, validated_data):
        text_filter_instance = validated_data.get('text_filter')
        filter_instances = validated_data['filters']
        category_instance = validated_data['category']
        user_id = validated_data['user_id']

        checkers = []
        with transaction.atomic():
            if text_filter_instance:
                text_filter_instance.save()

                checker = self.__create_checker_task(
                    category_instance=None,
                    filter_instances=text_filter_instance,
                    user_id=user_id,
                )

                checkers.append(checker)

            if category_instance:
                if filter_instances:
                    for filter_instance in filter_instances:
                        if filter_instance.type_name in [FilterType.MAX.value, FilterType.MIN.value]:
                            filter_instance.save()

                checker = self.__create_checker_task(
                    category_instance=category_instance,
                    filter_instances=filter_instances,
                    user_id=user_id,
                )

                checkers.append(checker)

        return checkers

    def __create_checker_task(self, category_instance, filter_instances, user_id):
        checker = Checker(category=category_instance)
        checker.save()

        if isinstance(filter_instances, Filter):
            checker.filters.add(filter_instances)
        else:
            checker.filters.set(filter_instances)

        checker.updated_at = timezone.now()
        checker.save(update_fields=('updated_at',))

        CheckerTask.objects.create_task(
            checker_name=CheckerTypeName.HOTLINE_UA.value,
            checker_id=checker.id,
            user_id=user_id,
        )

        return checker
