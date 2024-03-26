from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from django.views.generic.list import ListView
from rest_framework import status
from rest_framework.generics import UpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.task_manager.models import CheckerTask


class BaseCheckerListView(ListView):
    model_class = None
    template_name = None
    context_object_name = None
    checker_type = None

    def get_queryset(self):
        user = self.request.user
        checker_ids = CheckerTask.objects.filter(
            user_id=user.id,
            checker_type=self.checker_type.value
        ).values_list('checker_id')
        return self.model_class.objects.filter(pk__in=checker_ids)

    def get(self, request, *args, **kwargs):
        user = self.request.user
        if not user.is_authenticated:
            messages.warning(self.request, _('Invalid access. Please log in.'))
            return redirect(reverse('index'))

        return super().get(request, *args, **kwargs)

    class Meta:
        abstract = True


class BaseUpdateAPIView(UpdateAPIView):
    serializer_class = None
    delete_serializer_class = None
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
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
