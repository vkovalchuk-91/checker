from apps.common.permissions import IsActiveAndAuthenticated
from apps.common.views import BaseUpdateAPIView
from apps.hotline_ua.serializers import CheckerUpdateSerializer
from apps.hotline_ua.serializers import CheckerDeleteSerializer


class CheckerUpdateAPIView(BaseUpdateAPIView):
    serializer_class = CheckerUpdateSerializer
    delete_serializer_class = CheckerDeleteSerializer
    permission_classes = (IsActiveAndAuthenticated,)
