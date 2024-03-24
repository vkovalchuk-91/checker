from django.urls import path

from apps.uz_ticket_checker.views.checker_view import CheckersListView, checker_add
from apps.uz_ticket_checker.views.stations_view import StationsListView, stations_update
from apps.uz_ticket_checker.views.ticket_search_view import search_results_view

app_name = "uz_ticket_checker_app"
urlpatterns = [
    path("", search_results_view, name="search_results"),
    path("checker/", CheckersListView.as_view(), name="checker"),
    path("checker/add/", checker_add, name="checker_add"),
    path("stations/", StationsListView.as_view(), name="stations"),
    path("stations/update/", stations_update, name="stations_update"),
]
