from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.checker.models import BaseChecker


class BaseCheckerUpdateSerializer(serializers.ModelSerializer):
    model_class = BaseChecker
    user_model_class = User

    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        abstract = True

    def validate(self, attrs):
        try:
            checker = self.model_class.objects.get(id=attrs['id'])
        except (self.model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'id': _(f'Checker by id:{id} does not exist..')}
            )

        try:
            user = self.user_model_class.objects.get(id=attrs['user_id'])
            if checker.user.id != user.id or not user.is_superuser:
                raise ValueError
        except (self.user_model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'user': _(f'Invalid user or permissions.')}
            )

        return attrs

    def create(self, validated_data):
        instance_id = self.validated_data['id']
        is_active = self.validated_data['is_active']
        instance = self.model_class.objects.get(id=instance_id)
        instance.is_active = is_active
        instance.updated_at = timezone.now()
        instance.save(update_fields=('is_active', 'updated_at',))
        return instance
