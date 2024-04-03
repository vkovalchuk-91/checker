from enum import Enum, auto


class SeatType(Enum):
    CLASS_1 = 1, 'first', '1st class'
    CLASS_2 = 2, 'second', '2nd class'
    CLASS_3 = 3, 'third', '3rd class'

    DEFAULT = 0, 'default', 'other'

    @staticmethod
    def find_by_value(value):
        if not value:
            return SeatType.DEFAULT

        for seat_type in SeatType:
            if isinstance(value, int) and seat_type.value[0] == value:
                return seat_type
            if isinstance(value, str) and seat_type.value[1] == value:
                return seat_type

        return SeatType.DEFAULT
