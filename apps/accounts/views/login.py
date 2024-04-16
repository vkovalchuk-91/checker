from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.utils.translation import gettext_lazy as _

from apps.accounts.models import User


class CustomAuthenticationForm(AuthenticationForm):
    def clean(self):
        username = self.cleaned_data.get("username")
        if username:
            user = User.objects.filter(email=username).first()
            if user and not user.is_active:
                raise forms.ValidationError(
                    _("Account is inactive. Please contact an administrator for more information.")
                )

        return super().clean()


class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
