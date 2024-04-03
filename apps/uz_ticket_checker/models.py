from django.db import models
from django.utils.translation import gettext_lazy as _
from loguru import logger

from apps.common import TimeStampedMixin
from apps.accounts.models import BaseParameter
from apps.common.constants import SEAT_TYPES, WAGON_TYPES, STATIONS


class Station(TimeStampedMixin):
    express_3_id = models.BigAutoField(
        auto_created=True,
        primary_key=True,
        serialize=False,
        verbose_name=_("EXPRESS-3 ID")
    )
    name = models.CharField(_("station name"), max_length=150)
    country = models.ForeignKey(
        "Country",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name=_("country"),
        verbose_name=_("country"))
    weight = models.DecimalField(max_digits=4, decimal_places=1, verbose_name=_("weight"))
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active."
            "Unselect this instead of deleting accounts."
        ),
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _("station")
        verbose_name_plural = _("stations")


class Country(models.Model):
    name = models.CharField(_("country name"), max_length=150)


class TicketSearchParameter(BaseParameter):
    departure_station = models.ForeignKey(
        "Station",
        on_delete=models.CASCADE,
        null=False,
        related_name=_("departures"),
        verbose_name=_("departure station"))
    arrival_station = models.ForeignKey(
        "Station",
        on_delete=models.CASCADE,
        null=False,
        related_name=_("arrivals"),
        verbose_name=_("arrival station"))
    start_date = models.DateTimeField(_("start date"), null=False)
    end_date = models.DateTimeField(_("end date"), null=False)
    train_number = models.ManyToManyField("TrainNumber", related_name="train_numbers")
    wagon_type = models.ManyToManyField("WagonType", related_name="wagon_types")
    seat_type = models.ManyToManyField("SeatType", related_name="seat_types")


class TrainNumber(models.Model):
    train_number = models.CharField(_("train number"), max_length=50)


class WagonType(models.Model):
    wagon_type = models.CharField(_("wagon type"), max_length=50)


class SeatType(models.Model):
    seat_type = models.CharField(_("seat type"), max_length=50)
    seat_type_name = models.CharField(_("seat type name"), max_length=50)


# Get active stations info for using in checkers app
try:
    if Station.objects.filter(is_active=True).exists():
        stations = Station.objects.filter(is_active=True).order_by('-weight')
        for station in stations:
            STATIONS[station.express_3_id] = station.name
except Exception as e:
    logger.info(e)


# wagon types initializing
try:
    for wagon_type in WAGON_TYPES:
        if not WagonType.objects.filter(wagon_type=wagon_type).exists():
            wagon_type_obj = WagonType(wagon_type=wagon_type)
            wagon_type_obj.save()
except Exception as e:
    logger.info(e)


# Update wagon types from DB for using in checkers app
try:
    if WagonType.objects.exists():
        wagon_types = WagonType.objects.all()
        WAGON_TYPES.clear()
        for wagon_type in wagon_types:
            WAGON_TYPES.append(wagon_type.wagon_type)
except Exception as e:
    logger.info(e)


# seat types initializing
try:
    for seat_type in SEAT_TYPES:
        if not SeatType.objects.filter(seat_type=seat_type['seat_type']).exists():
            seat_type_obj = SeatType(seat_type=seat_type['seat_type'], seat_type_name=seat_type['seat_type_name'])
            seat_type_obj.save()
except Exception as e:
    logger.info(e)


# Update seat types from DB for using in checkers app
try:
    if SeatType.objects.exists():
        seat_types = SeatType.objects.all()
        SEAT_TYPES.clear()
        for seat_type in seat_types:
            SEAT_TYPES.append({'seat_type': seat_type.seat_type, 'seat_type_name': seat_type.seat_type_name})
except Exception as e:
    logger.info(e)
