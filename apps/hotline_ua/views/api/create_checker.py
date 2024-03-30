from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.common.permissions import IsActiveAndAuthenticated
from apps.hotline_ua.serializers import SearchParameterCreateSerializer
from apps.hotline_ua.serializers.create_checker import SearchParameterCreateSerializer
from apps.hotline_ua.tasks import run_checkers


class CheckerCreateAPIView(CreateAPIView):
    serializer_class = SearchParameterCreateSerializer
    permission_classes = (IsActiveAndAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        data['user_id'] = request.user.id
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        save_data = serializer.save()
        serializer_data = self.serializer_class(save_data, many=True).data

        if save_data:
            run_checkers.apply_async(args=([i.id for i in save_data],))
            # run_checkers([i.id for i in save_data])

        return Response(data=serializer_data, status=status.HTTP_200_OK)
