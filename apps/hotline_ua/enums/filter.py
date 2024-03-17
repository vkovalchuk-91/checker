from enum import Enum, auto


class FilterType(Enum):
    BRAND = 'brand'
    SHOP = 'shop'
    LINK = 'link'
    TEXT = 'text'
    MIN = 'min'
    MAX = 'max'

    @staticmethod
    def find_filter_by_value(value):
        if not value:
            return None

        for filter_type in FilterType:
            if filter_type.value == value:
                return filter_type

        return None
