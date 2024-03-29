from django.contrib import admin

from apps.tickets_ua.models import BaseSearchParameter, Station


# Register your models here.

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ...


@admin.register(BaseSearchParameter)
class BaseSearchParameterAdmin(admin.ModelAdmin):
    ...
