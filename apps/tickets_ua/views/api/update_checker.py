from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.tickets_ua.serializers.update_checker import CheckerUpdateSerializer
from apps.tickets_ua.serializers.delete_checker import CheckerDeleteSerializer


class CheckerUpdateAPIView(UpdateAPIView):
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        data = {**request.data, 'user_id': request.user.id}
        data.update({'id': self.kwargs['pk']})
        serializer = CheckerUpdateSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['pk']
        user_id = request.user.id
        serializer = CheckerDeleteSerializer(data={'id': _id, 'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
