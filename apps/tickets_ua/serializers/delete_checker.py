from apps.common.serializer import InstanceDeleteSerializer
from apps.tickets_ua.models import Checker


class CheckerDeleteSerializer(InstanceDeleteSerializer):
    model_class = Checker

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
