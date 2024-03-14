from datetime import datetime

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.tickets_ua.models import Station, Checker
from apps.tickets_ua.serializers.station import StationSerializer

DATA_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class CheckerCreateSerializer(serializers.ModelSerializer):
    from_station = StationSerializer()
    to_station = StationSerializer()
    date_at = serializers.CharField(required=True, help_text=_(f'Period in format "{DATA_FORMAT} - {DATA_FORMAT}".'))
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Checker
        fields = [
            'id',
            'from_station',
            'to_station',
            'date_at',
            'time_at',
            'user_id',
        ]
        extra_kwargs = {
            'time_at': {'required': True},
        }

    def validate(self, attrs):
        try:
            attrs['user'] = User.objects.get(id=attrs['user_id'])
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid user.')}
            )

        try:
            attrs['from_station'] = attrs['from_station']['station']
            if not attrs['from_station']:
                raise ValueError
        except (Station.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'from_station': _(f'Invalid from station.')}
            )

        try:
            attrs['to_station'] = attrs['to_station']['station']
            if not attrs['to_station']:
                raise ValueError
        except (Station.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'to_station': _(f'Invalid to station.')}
            )

        if attrs['from_station'].id == attrs['to_station'].id:
            raise serializers.ValidationError(
                {'station': _(f'Stations must be different.')}
            )

        try:
            date_at = attrs['date_at']
            if ' - ' in date_at:
                start_str, end_str = map(str.strip, attrs['date_at'].split(' - '))
                start_date = datetime.strptime(start_str, DATA_FORMAT)
                end_date = datetime.strptime(end_str, DATA_FORMAT)
            else:
                start_date = datetime.strptime(date_at, DATA_FORMAT)
                end_date = datetime.strptime(date_at, DATA_FORMAT)

            if start_date > end_date:
                raise ValueError

            attrs['start_date'] = start_date
            attrs['end_date'] = end_date
        except ValueError:
            raise serializers.ValidationError(
                {'date_at': _(f'Invalid date format: {DATA_FORMAT} (or range).')}
            )

        return attrs

    def create(self, validated_data):
        checkers = Checker.objects.create_checkers_in_range(
            from_station=validated_data['from_station'],
            to_station=validated_data['to_station'],
            start_date=validated_data['start_date'],
            end_date=validated_data['end_date'],
            time_at=validated_data['time_at'],
            user=validated_data['user'],
        )
        return checkers
