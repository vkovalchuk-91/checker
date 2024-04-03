from dataclasses import dataclass
from datetime import datetime

from apps.tickets_ua.enums.seat import SeatType


@dataclass
class Seat:
    type: SeatType
    available: int


@dataclass
class Transport:
    number: str
    name: str
    travel_time_minutes: int
    date_at: datetime
    seats: list[Seat]


class _TransportParser:
    result_class = Transport
    seat_class = Seat

    @property
    def result_items(self):
        return []

    class Meta:
        abstract = True
