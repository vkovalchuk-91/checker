from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.booking_uz_gov_ua.models import Checker

DATA_FORMAT = "%Y-%m-%d"
TIME_FORMAT = "%H:%M"


class CheckerUpdateSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Checker
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
        extra_kwargs = {
            'id': {'required': True},
            'is_active': {'required': True},
        }

    def validate(self, attrs):
        try:
            checker = Checker.objects.get(id=attrs['id'])
        except (Checker.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'id': _(f'Checker by id:{id} does not exist..')}
            )

        try:
            user = User.objects.get(id=attrs['user_id'])
            if checker.user.id != user.id or not user.is_superuser:
                raise ValueError
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid user or permissions.')}
            )

        return attrs

    def create(self, validated_data):
        instance_id = self.validated_data['id']
        is_active = self.validated_data['is_active']
        instance = Checker.objects.get(id=instance_id)
        instance.is_active = is_active
        instance.save(update_fields=['is_active'])
        return instance
