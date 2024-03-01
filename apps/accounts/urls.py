from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views.confirm_email_complete import ConfirmEmailCompleteView
from apps.accounts.views.signup import SignUpView

app_name = "accounts"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("confirm-email/<str:uid>/<str:token>/", ConfirmEmailCompleteView.as_view(), name="confirm_email"),
]