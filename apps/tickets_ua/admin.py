from django.contrib import admin

from apps.tickets_ua.models import Checker, Station


# Register your models here.

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ...


@admin.register(Checker)
class CheckerAdmin(admin.ModelAdmin):
    ...
