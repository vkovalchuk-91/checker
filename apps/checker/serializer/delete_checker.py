from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.checker.models import BaseChecker


class BaseCheckerDeleteSerializer(serializers.ModelSerializer):
    model_class = BaseChecker
    user_model_class = User

    id = serializers.IntegerField(required=True)
    user_id = serializers.IntegerField(required=True)

    class Meta:
        fields = [
            'id',
            'user_id',
        ]
        extra_kwargs = {
            'id': {'required': True},
            'user_id': {'required': True},
        }
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

    def delete(self):
        instance_id = self.validated_data['id']
        instance = self.model_class.objects.get(id=instance_id)
        instance.delete()
