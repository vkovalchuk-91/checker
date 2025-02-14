from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.common.permissions import IsActiveAndAuthenticated
from apps.hotline_ua.serializers import FilterCreateSerializer


class FilterCreateAPIView(CreateAPIView):
    serializer_class = FilterCreateSerializer
    permission_classes = (IsActiveAndAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        save_date = serializer.save()
        serializer_date = self.serializer_class(save_date, many=True).data
        return Response(data=serializer_date, status=status.HTTP_201_CREATED)
