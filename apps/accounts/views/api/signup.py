from django.db import transaction
from django.shortcuts import render
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from apps.accounts.permissions.anonymous import IsAnonymous
from apps.accounts.serializers import SignUpSerializer
from apps.accounts.tasks import send_email_confirmation


class SignUpView(CreateAPIView):
    serializer_class = SignUpSerializer
    permission_classes = (IsAnonymous,)
    template_name = 'registration/signup.html'

    @extend_schema(
        request=serializer_class,
        responses={status.HTTP_204_NO_CONTENT: None},
    )
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        with transaction.atomic():
            user = serializer.save()
            if not user.is_email_verified:
                transaction.on_commit(lambda: send_email_confirmation.apply_async(args=(user.id,)))

        return Response(status=status.HTTP_204_NO_CONTENT)

    @extend_schema(
        responses={status.HTTP_200_OK: None},
    )
    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
