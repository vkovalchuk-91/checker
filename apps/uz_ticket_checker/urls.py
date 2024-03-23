from django.urls import path

from apps.uz_ticket_checker.views.stations_update import stations_update
from apps.uz_ticket_checker.views.uz_ticket_checker import UzTicketCheckerListView

app_name = "uz_ticket_checker_app"
urlpatterns = [
    path("", UzTicketCheckerListView.as_view(), name="index"),
    path("stations/update/", stations_update, name="stations_update"),
]
