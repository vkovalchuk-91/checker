from apps.common.views import BaseUpdateAPIView
from apps.tickets_ua.serializers.delete_checker import CheckerDeleteSerializer
from apps.tickets_ua.serializers.update_checker import CheckerUpdateSerializer


class CheckerUpdateAPIView(BaseUpdateAPIView):
    serializer_class = CheckerUpdateSerializer
    delete_serializer_class = CheckerDeleteSerializer
