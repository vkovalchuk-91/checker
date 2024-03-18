from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User


class InstanceStateUpdateSerializer(serializers.ModelSerializer):
    model_class = None
    user_model_class = User

    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        abstract = True

    def validate(self, attrs):
        try:
            instance = self.model_class.objects.get(id=attrs['id'])
        except (self.model_class.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'id': _(f'Checker by id:{id} does not exist..')}
            )

        try:
            user_instance = self.user_model_class.objects.get(id=attrs['user_id'])
            if instance.user.id != user_instance.id and not user_instance.is_superuser:
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
