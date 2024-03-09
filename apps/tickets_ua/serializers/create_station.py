from django.db.models import Q
from rest_framework import serializers

from apps.tickets_ua.models import Station


class StationCreateSerializer(serializers.ModelSerializer):
    title = serializers.CharField(required=True, min_length=2)

    class Meta:
        model = Station
        fields = (
            'title',
            'value',
        )
        extra_kwargs = {
            'title': {'required': True},
        }

    def validate(self, attrs):
        title = attrs.get('title')
        stations = list(Station.objects.filter(
            Q(title__contains=title) | Q(title__contains=title.capitalize())
        ))

        attrs['stations'] = stations
        return attrs

    def create(self, validated_data):
        stations = validated_data.pop('stations')
        return stations
