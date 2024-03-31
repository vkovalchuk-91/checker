from django.urls import path

from apps.uz_ticket_checker.views.checker_view import checker_add, checkers_view, checker_check, checker_delete, \
    checker_change_is_active
from apps.uz_ticket_checker.views.stations_view import StationsListView, stations_update
from apps.uz_ticket_checker.views.ticket_search_view import search_results_view, execute_task

app_name = "uz_ticket_checker_app"
urlpatterns = [
    path("", search_results_view, name="search_results"),
    path("execute_task/", execute_task, name="execute_task"),
    path("checker/", checkers_view, name="checker"),
    path("checker/check/", checker_check, name="checker_check"),
    path("checker/add/", checker_add, name="checker_add"),
    path("checker/delete/<int:pk>/", checker_delete, name="checker_delete"),
    path("checker/change_is_active/<int:pk>/", checker_change_is_active, name="checker_change_is_active"),
    path("stations/", StationsListView.as_view(), name="stations"),
    path("stations/update/", stations_update, name="stations_update"),
]
