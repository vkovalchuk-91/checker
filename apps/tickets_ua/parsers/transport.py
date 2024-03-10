from dataclasses import dataclass
from datetime import datetime

from apps.tickets_ua.enums.seat_type import SeatType


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

    @staticmethod
    def get_seat_type_by_value(value) -> SeatType:
        if not value:
            return SeatType.DEFAULT

        for seat_type in SeatType:
            if isinstance(value, int) and seat_type.value[0] == value:
                return seat_type
            if isinstance(value, str) and seat_type.value[1] == value:
                return seat_type

        return SeatType.DEFAULT
