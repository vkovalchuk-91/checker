from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.hotline_ua.serializers.create_filter import CreateFilterSerializer
from apps.hotline_ua.tasks import scraping_categories_filters


class CreateFilterAPIView(CreateAPIView):
    serializer_class = CreateFilterSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)

        save_date = serializer.save()
        filters = save_date.pop('filters')
        if len(filters) == 0 or (len(filters) == 1 and filters[0].title != data['title']):
            category = save_date.pop('category')
            scraping_categories_filters.apply_async(args=([category['id']],))

        serializer_date = self.serializer_class(filters, many=True).data
        return Response(data=serializer_date, status=status.HTTP_200_OK)
