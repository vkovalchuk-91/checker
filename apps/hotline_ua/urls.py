from django.urls import path

from apps.hotline_ua.views import api
from apps.hotline_ua.views.checker import CheckerListView

app_name = "hotline_ua"
urlpatterns = [
    path("", CheckerListView.as_view(), name="index"),

    path("api/catalog/", api.CreateCategoryAPIView.as_view(), name="api-category"),
    path("api/filter/", api.CreateFilterAPIView.as_view(), name="api-filter"),
    path("api/checker/", api.CreateCheckerAPIView.as_view(), name="api-checker"),
    path("api/checker/<int:pk>/", api.UpdateCheckerAPIView.as_view(), name='api-update-checker'),
]
