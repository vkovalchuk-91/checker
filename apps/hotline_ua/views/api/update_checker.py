from apps.common.views import BaseUpdateAPIView
from apps.hotline_ua.serializers import CheckerUpdateSerializer
from apps.hotline_ua.serializers.delete_checker import CheckerDeleteSerializer


class CheckerUpdateAPIView(BaseUpdateAPIView):
    serializer_class = CheckerUpdateSerializer
    delete_serializer_class = CheckerDeleteSerializer
