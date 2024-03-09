from django.contrib.auth.tokens import default_token_generator
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User
from apps.accounts.utils.security import decode_uid


class ConfirmEmailSerializer(serializers.Serializer):
    uid = serializers.CharField(required=True)
    token = serializers.CharField(required=True)

    def validate(self, attrs):
        uid = attrs.get('uid')
        token = attrs.get('token')

        try:
            user_id = decode_uid(uid)
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise serializers.ValidationError(
                {'uid': _('Invalid uid')},
                code='invalid_uid'
            )

        if user.is_email_verified:
            raise serializers.ValidationError(
                {'email': _('Email is already verified')},
                code='email_already_verified'
            )

        if not default_token_generator.check_token(user, token):
            raise serializers.ValidationError(
                {'token': _('Invalid token')},
                code='invalid_token'
            )

        attrs['user'] = user
        return attrs

    def create(self, validated_data):
        user = validated_data['user']
        user.is_email_verified = True
        user.updated_at = timezone.now()
        user.save(update_fields=('is_email_verified', 'updated_at'))
        return user
