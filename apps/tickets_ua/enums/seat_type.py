from enum import Enum, auto


class SeatType(Enum):
    CLASS_1 = 1, 'first', '1st class '
    CLASS_2 = 2, 'second', '2nd class'
    CLASS_3 = 3, 'third', '3rd class'

    DEFAULT = 0, 'default' 'other'
