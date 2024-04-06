from django.contrib.auth import views as auth_views
from django.urls import path

from apps.accounts.views import api

app_name = "accounts"
urlpatterns = [
    path("login/", auth_views.LoginView.as_view(), name="login"),
    path("logout/", auth_views.LogoutView.as_view(), name="logout"),
    path("signup/", api.SignUpView.as_view(), name="signup"),
    path("telegram/", api.SignUpView.as_view(), name="telegram"),
    path("confirm-email/<str:uid>/<str:token>/", api.ConfirmEmailCompleteView.as_view(), name="confirm_email"),
]
