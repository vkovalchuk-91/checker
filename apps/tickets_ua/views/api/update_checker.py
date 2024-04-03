from apps.common.permissions import IsActiveAndAuthenticated
from apps.common.views import BaseUpdateAPIView
from apps.tickets_ua.serializers.delete_checker import CheckerDeleteSerializer
from apps.tickets_ua.serializers.update_checker import TicketsUaCheckerUpdateSerializer


class CheckerUpdateAPIView(BaseUpdateAPIView):
    serializer_class = TicketsUaCheckerUpdateSerializer
    delete_serializer_class = CheckerDeleteSerializer
    permission_classes = (IsActiveAndAuthenticated,)
