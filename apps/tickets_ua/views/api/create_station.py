from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tickets_ua.serializers.create_station import StationCreateSerializer
from apps.tickets_ua.tasks import scraping_train_stations


class StationCreateAPIView(CreateAPIView):
    serializer_class = StationCreateSerializer
    permission_classes = (IsAuthenticated,)

    def create(self, request, *args, **kwargs):
        data = {**request.data, **self.kwargs}
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        save_date = serializer.save()

        if len(save_date) == 0 or (len(save_date) == 1 and save_date[0].name != data['name']):
            scraping_train_stations.apply_async(args=(data['name'],))

        serializer_date = StationCreateSerializer(save_date, many=True).data
        return Response(data=serializer_date, status=status.HTTP_200_OK)
