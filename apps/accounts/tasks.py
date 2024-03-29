from datetime import datetime
from urllib.parse import urljoin

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator

from apps.celery import celery_app as app
from apps.accounts.models import User
from apps.accounts.utils.security import encode_uid
from apps.common.emails import send_email


@app.task(name='send_email_confirmation')
def send_email_confirmation(user_id: int):
    user = User.objects.only('email', 'first_name', 'last_name').get(pk=user_id)
    user.last_login = datetime.now()
    user.save(update_fields=('last_login',))

    uid = encode_uid(user_id)
    token = default_token_generator.make_token(user)

    link = urljoin(
        settings.FRONTEND_HOST,
        settings.FRONTEND_CONFIRM_EMAIL_PATH.format(uid=uid, token=token)
    )
    send_email(
        subject='Confirm email',
        body=f'Pleas click on {link} below to confirm your email',
        to=[user.email],
    )


@app.task(name='send_email_oauth_password_generated')
def send_email_oauth_password_generated(email: str, password: str):
    send_email(
        subject='Auto generate password',
        body=f'For you email {email} auto generated password <b>{password}<b>.',
        to=[email],
    )


@app.task(name='send_email_checker_result_msg')
def send_email_checker_result_msg(user_id: int, msg: str):
    user = User.objects.only('email', 'first_name', 'last_name').get(pk=user_id)
    send_email(
        subject='Checker result message',
        body=f'{msg}',
        to=[user.email],
    )
