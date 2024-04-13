import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):
    first_name = serializers.RegexField(
        regex=r'^[a-zA-Zа-яА-ЯіїІЇєЄ\s\'-]{2,30}$',
        required=True,
        error_messages={
            'invalid': _(
                'Valid length is from 2 to 30 characters. Only letters of the alphabet (Latin or Cyrillic), spaces, hyphens and apostrophes are allowed.')
        }
    )
    last_name = serializers.RegexField(
        regex=r'^[a-zA-Zа-яА-ЯіїІЇєЄ\s\'-]{2,30}$',
        required=True,
        error_messages={
            'invalid': _(
                'Valid length is from 2 to 30 characters. Only letters of the alphabet (Latin or Cyrillic), spaces, hyphens and apostrophes are allowed.')
        }
    )
    password = serializers.CharField(required=True, min_length=8, )
    confirm = serializers.CharField(required=False, min_length=8, )

    class Meta:
        model = User = get_user_model()
        fields = (
            'email',
            'password',
            'first_name',
            'last_name',
            'confirm'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
            'confirm': {'required': False},
        }

    def validate_email(self, email):
        email_pattern = r"^[a-zA-Z0-9._%+-]{2,64}@[a-zA-Z0-9.-]{4,255}$"
        if not re.match(email_pattern, email, re.IGNORECASE):
            raise serializers.ValidationError(
                {'email': _(f'Not valid email {email}.')}
            )

        if User.objects.filter(email=email).exists():
            raise serializers.ValidationError(
                {'email': _(f'User with email {email} exist.')}
            )

        return email

    def validate_password(self, password):
        if not self.initial_data.get('confirm') or password != self.initial_data.get('confirm'):
            raise serializers.ValidationError(
                {'password': _(f'Password and confirm not equals.')}
            )
        return password

    def create(self, validated_data):
        password = validated_data.pop('password')
        validated_data.pop('confirm')
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save(update_fields=('password', 'updated_at'))
        return user
