import re

from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.tickets_ua.models import Station
from apps.tickets_ua.tasks import scraping_train_stations, scraping_bus_station_name

DATA_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class StationSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=100)

    class Meta:
        model = Station
        fields = [
            'name',
            'code',
        ]
        extra_kwargs = {
            'name': {'required': True},
            'code': {'required': False},
        }

    def validate(self, attrs):
        name = attrs['name']

        pattern = re.compile(r'^[а-яії0-9\'. ]+$')
        if not bool(pattern.match(name.lower())):
            raise serializers.ValidationError(
                {'name': _(f'Invalid name.')}
            )

        try:
            if name.isdigit() and len(name) > 4 and int(name) > 0:
                station = Station.objects.get(code=name, )
            else:
                try:
                    station = Station.objects.get(name=name, )
                except Station.DoesNotExist:
                    scraping_train_stations(title=name)
                    station = Station.objects.get(name=name, )
        except Station.DoesNotExist:
            raise serializers.ValidationError(
                {'station': _(f'Invalid station.')}
            )

        if not station.bus_name or station.bus_name == '':
            _id = station.id
            station.bus_name = scraping_bus_station_name(_id)

        attrs['name'] = station.name
        attrs['code'] = station.code
        attrs['station'] = station

        return attrs
