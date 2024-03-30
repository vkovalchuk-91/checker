from django.contrib import messages
from django.shortcuts import redirect, reverse
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from apps.accounts.serializers.confirm_email_complete import ConfirmEmailSerializer


class ConfirmEmailCompleteView(GenericAPIView):
    serializer_class = ConfirmEmailSerializer
    permission_classes = (AllowAny,)

    def get(self, request, *args, **kwargs):
        uid = self.kwargs['uid']
        token = self.kwargs['token']
        serializer = self.get_serializer(data={'uid': uid, 'token': token})
        try:
            serializer.is_valid(raise_exception=True)
            serializer.save()
            messages.info(request, _('Confirm email complete successfully.'))
        except serializers.ValidationError as e:
            messages.error(request, f'{e.detail}')

        return redirect(reverse('index'))
