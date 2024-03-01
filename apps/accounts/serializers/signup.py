import re

from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from apps.accounts.models import User


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User = get_user_model()
        fields = (
            'email',
            'password',
            'first_name',
            'last_name'
        )
        extra_kwargs = {
            'email': {'required': True},
            'password': {'required': True},
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, email):
        email_pattern = r"^[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}$"
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
        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save(update_fields=('password', 'updated_at'))
        return user
