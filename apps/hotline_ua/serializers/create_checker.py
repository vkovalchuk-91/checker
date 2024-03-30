from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import ParameterCategory, BaseParameter
from apps.common.enums.checker_name import CheckerTypeName
from apps.hotline_ua.enums.filter import FilterType
from apps.hotline_ua.models import BaseSearchParameter, Filter
from apps.hotline_ua.serializers.base_category import CategorySerializer
from apps.hotline_ua.serializers.base_filter_ import FilterInstanceSerializer
from apps.task_manager.models import CheckerTask


class SearchParameterCreateSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    filters = FilterInstanceSerializer(many=True)
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = BaseSearchParameter
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

        category = attrs['category']
        if not category.get('id') and len(attrs['filters']) == 0:
            raise serializers.ValidationError(
                {'parameters': _(f'Invalid empty search parameter(s).')}
            )

        filter_instances: list[Filter] = [element['instance'] for element in attrs['filters']]
        new_filters_count = len([element for element in filter_instances if element.type_name == FilterType.TEXT.value])
        if category.get('id'):
            new_filters_count += 1

        if not CheckerTask.objects.can_create_new_task(attrs['user_id'], need_count=new_filters_count):
            raise serializers.ValidationError(
                {'task': _(f'Cannot create {new_filters_count} search task(s).')}
            )

        attrs['instances'] = filter_instances
        return attrs

    def create(self, validated_data):
        filter_instances: list[Filter] = validated_data['instances']
        category_id = validated_data['category'].get('id')
        user_id = validated_data['user_id']

        checkers = []
        with transaction.atomic():
            filter_list = []
            for filter_instance in filter_instances:
                filter_type = FilterType.find_by_value(filter_instance.type_name)
                if filter_type and filter_type == FilterType.TEXT:
                    filter_instance.save()
                    checker = self.__create_checker_task(
                        category_id=None,
                        filter_instances=filter_instance,
                        user_id=user_id,
                    )
                    checkers.append(checker)
                else:
                    if filter_type and filter_type in (FilterType.MAX, FilterType.MIN, FilterType.LINK):
                        filter_instance.save()
                    filter_list.append(filter_instance)

            if category_id:
                checker = self.__create_checker_task(
                    category_id=category_id,
                    filter_instances=filter_list,
                    user_id=user_id,
                )
                checkers.append(checker)

        return checkers

    def __create_checker_task(self, category_id, filter_instances, user_id):
        param_category, created = ParameterCategory.objects.get_or_create(
            param_category_name=CheckerTypeName.HOTLINE_UA.value
        )
        param_type = BaseParameter.objects.create(param_type=param_category)
        if not category_id:
            checker = BaseSearchParameter(
                category=None,
                param_type=param_type
            )
        else:
            checker = BaseSearchParameter(
                category_id=category_id,
                param_type=param_type
            )
        checker.save()

        if filter_instances:
            if isinstance(filter_instances, Filter):
                checker.filters.add(filter_instances)
            else:
                checker.filters.set(filter_instances)

            checker.updated_at = timezone.now()
            checker.save(update_fields=('updated_at',))

        CheckerTask.objects.create(
            task_param_id=param_type.id,
            user_id=user_id,
        )

        return checker
