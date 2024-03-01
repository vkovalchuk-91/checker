from django.contrib import messages
from django.db import transaction
from django.shortcuts import redirect, reverse, render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import CreateAPIView

from apps.accounts.permissions.anonymous import IsAnonymous
from apps.accounts.serializers import SignUpSerializer
from apps.accounts.tasks import send_email_confirmation


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (IsAnonymous,)
    template_name = 'registration/signup.html'

    def create(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()
            if not user.is_email_verified:
                transaction.on_commit(lambda: send_email_confirmation.apply_async(args=(user.id,)))

        return Response(status=status.HTTP_204_NO_CONTENT)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
