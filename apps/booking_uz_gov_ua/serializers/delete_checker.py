from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.booking_uz_gov_ua.models import Checker


class CheckerDeleteSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        model = Checker
        fields = [
            'id',
            'user_id',
        ]
        extra_kwargs = {
            'id': {'required': True},
            'user_id': {'required': True},
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

    def delete(self):
        instance_id = self.validated_data['id']
        instance = Checker.objects.get(id=instance_id)
        instance.delete()
