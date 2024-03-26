from apps.common.enums.checker_name import CheckerTypeName
from apps.common.serializer import DeleteSerializer
from apps.tickets_ua.models import Checker


class CheckerDeleteSerializer(DeleteSerializer):
    model_class = Checker
    checker_type = CheckerTypeName.TICKETS_UA

    class Meta:
        model = Checker
        fields = [
            'id',
            'user_id',
        ]
