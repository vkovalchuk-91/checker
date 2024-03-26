from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import UpdateSerializer
from apps.hotline_ua.models import Checker


class CheckerUpdateSerializer(UpdateSerializer):
    model_class = Checker
    checker_type = CheckerTypeName.HOTLINE_UA

    class Meta:
        model = Checker
        fields = [
            'id',
            'is_active',
            'user_id',
        ]
