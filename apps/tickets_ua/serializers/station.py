from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.tickets_ua.models import Station
from apps.tickets_ua.tasks import scraping_uz_stations

DATA_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class StationSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=100)

    class Meta:
        model = Station
        fields = [
            'title',
            'value',
        ]
        extra_kwargs = {
            'title': {'required': True},
            'value': {'required': False},
        }

    def validate(self, attrs):
        title = attrs['title']

        try:
            if title.isdigit() and len(title) > 4 and int(title) > 0:
                station = Station.objects.get(value=title, )
            else:
                try:
                    station = Station.objects.get(title=title, )
                except Station.DoesNotExist:
                    scraping_uz_stations(title=title)
                    station = Station.objects.get(title=title, )
        except Station.DoesNotExist:
            raise serializers.ValidationError(
                {'station': _(f'Invalid to station.')}
            )

        attrs['title'] = station.title
        attrs['value'] = station.value
        attrs['station'] = station

        return attrs
