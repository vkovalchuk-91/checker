from apps.common.serializer import InstanceStateUpdateSerializer
from apps.tickets_ua.models import Checker


class CheckerUpdateSerializer(InstanceStateUpdateSerializer):
    model_class = Checker

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
