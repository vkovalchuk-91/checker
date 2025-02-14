from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response


class BaseUpdateAPIView(GenericAPIView):
    serializer_class = None
    delete_serializer_class = None

    def put(self, request, *args, **kwargs):
        data = {**request.data, 'user_id': request.user.id}
        data.update({'id': self.kwargs['pk']})
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(data=serializer.data, status=status.HTTP_200_OK)

    def delete(self, request, *args, **kwargs):
        _id = self.kwargs['pk']
        user_id = request.user.id
        serializer = self.delete_serializer_class(data={'id': _id, 'user_id': user_id})
        serializer.is_valid(raise_exception=True)
        serializer.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    class Meta:
        abstract = True
