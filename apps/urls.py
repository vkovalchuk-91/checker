"""
URL configuration for task_1 project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

from apps.views import index, telegram, feedback, redirect_to_index_page

urlpatterns = [
    path("", index, name="index"),
    path("", include('apps.tbot_base.urls')),  # include webhook url
    path("telegram/", telegram, name="telegram"),
    path("feedback/", feedback, name="feedback"),

    path('i18n/', include('django.conf.urls.i18n')),

    path("uz_ticket/", include('apps.uz_ticket_checker.urls'), name="uz_ticket_checker"),
    path("tickets_ua/", include('apps.tickets_ua.urls'), name="tickets_ua"),
    path("hotline_ua/", include('apps.hotline_ua.urls'), name="hotline_ua"),

    path('admin/', admin.site.urls, name="admin"),
    path('accounts/', include('apps.accounts.urls'), name="accounts"),

    path('oauth2/inactive/', redirect_to_index_page),
    path('oauth2/', include('allauth.urls')),
    # path('oauth2/', include('allauth.socialaccount.urls')),

    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/schema/swagger/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger'),
    path('api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]
