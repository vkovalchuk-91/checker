from django.urls import path

from apps.booking_uz_gov_ua.views import api
from apps.booking_uz_gov_ua.views.checker import CheckerListView

app_name = "uz"
urlpatterns = [
    path("", CheckerListView.as_view(), name="index"),

    path("api/station/", api.StationCreateAPIView.as_view(), name="api-station"),
    path("api/checker/", api.CheckerCreateAPIView.as_view(), name="api-checker"),
    path("api/checker/<int:pk>/", api.CheckerUpdateAPIView.as_view(), name='api-checker-update'),
]
