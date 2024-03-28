from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.common.constants import TITLE_REGEX_DEFAULT
from apps.tickets_ua.models import Station
from apps.tickets_ua.tasks import scraping_train_stations


class StationSerializer(serializers.ModelSerializer):
    # name = serializers.CharField(max_length=100)
    name = serializers.RegexField(required=True, regex=TITLE_REGEX_DEFAULT)
    code = serializers.IntegerField(required=False, allow_null=True)

    class Meta:
        model = Station
        fields = [
            'id',
            'name',
            'code',
        ]
        # extra_kwargs = {
        #     'name': {'required': True},
        #     'code': {'required': False},
        # }

    def validate(self, attrs):
        code = attrs.get('code')
        if code and Station.objects.filter(code=code).count() == 1:
            attrs['id'] = Station.objects.get(code=code).id
            return attrs

        name = attrs['name']
        if name.isdigit() and len(name) > 4 and int(name) > 0 and Station.objects.filter(code=int(name)).count() == 1:
            attrs['id'] = Station.objects.get(code=int(name)).id
            return attrs

        count = Station.objects.filter(name=name, ).count()
        if count == 1:
            attrs['id'] = Station.objects.get(name=name).id
            return attrs
        elif count > 1:
            raise serializers.ValidationError(
                {'station': _(f'Invalid station.')}
            )

        scraping_train_stations(title=name)
        try:
            attrs['id'] = Station.objects.get(name=name, )
        except (Station.MultipleObjectsReturned, Station.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'station': _(f'Invalid station.')}
            )

        return attrs
