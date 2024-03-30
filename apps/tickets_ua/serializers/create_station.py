import re

from django.db.models import Q
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.tickets_ua.models import Station


class StationCreateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(required=True, min_length=2, max_length=100)

    class Meta:
        model = Station
        fields = (
            'name',
            'code',
        )
        extra_kwargs = {
            'name': {'required': True},
        }

    def validate(self, attrs):
        name = attrs.get('name')

        pattern = re.compile(r'^[а-яії0-9\'. ]+$')
        if not bool(pattern.match(name.lower())):
            raise serializers.ValidationError(
                {'name': _(f'Invalid name.')}
            )
        stations = list(Station.objects.filter(
            Q(name__contains=name) | Q(name__contains=name.capitalize())
        ))

        attrs['instances'] = stations if stations else []
        return attrs

    def create(self, validated_data):
        instances = validated_data.pop('instances')
        return instances
