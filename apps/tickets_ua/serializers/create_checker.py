from datetime import datetime

from django.db import transaction
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User, ParameterCategory, BaseParameter
from apps.common.constants import DATA_FORMAT_DEFAULT
from apps.common.enums.checker_name import CheckerTypeName
from apps.task_manager.models import CheckerTask
from apps.tickets_ua.models import BaseSearchParameter
from apps.tickets_ua.serializers.station import StationSerializer


class CheckerCreateSerializer(serializers.ModelSerializer):
    from_station = StationSerializer()
    to_station = StationSerializer()
    date_at = serializers.CharField(required=True,
                                    help_text=_(f'Period in format "{DATA_FORMAT_DEFAULT} - {DATA_FORMAT_DEFAULT}".'))
    user_id = serializers.IntegerField(required=False)

    class Meta:
        model = BaseSearchParameter
        fields = [
            'id',
            'from_station',
            'to_station',
            'date_at',
            'time_at',
            'user_id',
        ]

    def validate(self, attrs):
        if not attrs.get('user_id') or not User.objects.filter(id=attrs['user_id']).exists():
            raise serializers.ValidationError(
                {'user': _(f'Invalid user.')}
            )

        if attrs['from_station']['id'] == attrs['to_station']['id']:
            raise serializers.ValidationError(
                {'station': _(f'Stations must be different.')}
            )

        try:
            date_at = attrs['date_at']
            if ' - ' in date_at:
                start_str, end_str = map(str.strip, attrs['date_at'].split(' - '))
                start_date = datetime.strptime(start_str, DATA_FORMAT_DEFAULT)
                end_date = datetime.strptime(end_str, DATA_FORMAT_DEFAULT)
            else:
                start_date = datetime.strptime(date_at, DATA_FORMAT_DEFAULT)
                end_date = datetime.strptime(date_at, DATA_FORMAT_DEFAULT)

            if start_date > end_date:
                raise ValueError

            attrs['start_date'] = start_date
            attrs['end_date'] = end_date
        except ValueError:
            raise serializers.ValidationError(
                {'dates': _(f'Invalid date in format: {DATA_FORMAT_DEFAULT} (or range).')}
            )

        now = timezone.now().date()
        if start_date.date() < now or end_date.date() < now:
            raise serializers.ValidationError(
                {'dates': _(f'Dates cannot be in past.')}
            )

        new_filters_count = (end_date - start_date).days
        if not CheckerTask.objects.can_create_new_task(attrs['user_id'], need_count=new_filters_count):
            raise serializers.ValidationError(
                {'checker': _(f'Cannot create {new_filters_count} checker(s).')}
            )

        return attrs

    def create(self, validated_data):
        user_id = validated_data['user_id']
        instances = BaseSearchParameter.objects.get_models_in_range(
            from_id=validated_data['from_station']['id'],
            to_id=validated_data['to_station']['id'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            time_at=validated_data['time_at'],
            user_id=user_id,
        )
        if len(instances) > 0:
            with transaction.atomic():
                param_category, created = ParameterCategory.objects.get_or_create(
                    param_category_name=CheckerTypeName.TICKETS_UA.value
                )
                for instance in instances:
                    param_type = BaseParameter.objects.create(param_type=param_category)
                    instance.param_type = param_type
                    instance.save()
                    CheckerTask.objects.create(
                        task_param_id=instance.param_type.id,
                        user_id=user_id,
                    )

        return instances
