from django.contrib import admin

from apps.booking_uz_gov_ua.models import Checker, Place, Station, Train


# Register your models here.

@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ...


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    ...


@admin.register(Train)
class TrainAdmin(admin.ModelAdmin):
    ...


@admin.register(Checker)
class CheckerAdmin(admin.ModelAdmin):
    ...
