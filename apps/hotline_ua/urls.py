from django.urls import path

from apps.hotline_ua.views import api
from apps.hotline_ua.views.checker import CheckerListView

app_name = "hotline_ua"
urlpatterns = [
    path("", CheckerListView.as_view(), name="index"),

    path("api/category/", api.CategoryCreateAPIView.as_view(), name="api-category"),
    path("api/filter/", api.FilterCreateAPIView.as_view(), name="api-filter"),
    path("api/checker/", api.CheckerCreateAPIView.as_view(), name="api-checker"),
    path("api/checker/<int:pk>/", api.HotlineUaCheckerUpdateAPIView.as_view(), name='api-update-checker'),
]
