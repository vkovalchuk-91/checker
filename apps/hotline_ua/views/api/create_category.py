from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.common.permissions import IsActiveAndAuthenticated
from apps.hotline_ua.serializers import CategoryCreateSerializer

from apps.hotline_ua.tasks import scraping_categories


class CategoryCreateAPIView(CreateAPIView):
    serializer_class = CategoryCreateSerializer
    permission_classes = (IsActiveAndAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        save_date = serializer.save()

        if len(save_date) == 0 or (len(save_date) == 1 and save_date[0].title != data['title']):
            scraping_categories.apply_async()

        serializer_date = self.serializer_class(save_date, many=True).data
        return Response(data=serializer_date, status=status.HTTP_201_CREATED)
