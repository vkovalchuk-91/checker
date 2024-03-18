from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hotline_ua.serializers import FilterCreateSerializer


class CreateFilterAPIView(CreateAPIView):
    serializer_class = FilterCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        save_date = serializer.save()
        serializer_date = self.serializer_class(save_date, many=True).data
        return Response(data=serializer_date, status=status.HTTP_200_OK)
