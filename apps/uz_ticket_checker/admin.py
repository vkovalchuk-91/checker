from django.contrib import admin

from apps.uz_ticket_checker.models import Station, Country, SeatType, WagonType, TrainNumber, TicketSearchParameter


@admin.register(Station)
class StationAdmin(admin.ModelAdmin):
    ...


@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    ...


@admin.register(TicketSearchParameter)
class TicketSearchParameterAdmin(admin.ModelAdmin):
    ...


@admin.register(TrainNumber)
class TrainNumberAdmin(admin.ModelAdmin):
    ...


@admin.register(WagonType)
class WagonTypeAdmin(admin.ModelAdmin):
    ...


@admin.register(SeatType)
class SeatTypeAdmin(admin.ModelAdmin):
    ...
