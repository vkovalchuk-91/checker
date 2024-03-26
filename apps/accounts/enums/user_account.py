from enum import Enum


class UserAccountType(Enum):
    REGISTERED_USER = 'registered'
    REGULAR_REGISTERED_USER = 'regular'
    VIP_REGISTERED_USER = 'vip'

    @staticmethod
    def find_by_value(value):
        if not value:
            return None

        for filter_type in UserAccountType:
            if filter_type.value == value:
                return filter_type

        return None
