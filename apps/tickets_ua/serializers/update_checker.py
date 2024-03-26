from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import UpdateSerializer
from apps.tickets_ua.models import Checker


class CheckerUpdateSerializer(UpdateSerializer):
    model_class = Checker
    checker_type = CheckerTypeName.TICKETS_UA

    class Meta:
        model = Checker
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
