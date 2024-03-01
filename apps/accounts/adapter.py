from allauth.account.adapter import DefaultAccountAdapter

from apps.accounts.tasks import send_email_oauth_password_generated


class GoogleAccountAdapter(DefaultAccountAdapter):

    def populate_username(self, request, user):
        user.is_email_verified = True
        email = user.email
        password = user.password
        user.set_password(password)
        send_email_oauth_password_generated.apply_async(args=(email, password,))
        super().populate_username(request, user)
        super().populate_username(request, user)
