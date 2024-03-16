from enum import Enum, auto


class FilterType(Enum):
    BRAND = 'brand'
    SHOP = 'shop'
    LINK = 'link'
    TEXT = 'text'
    MIN_PRICE = 'min price'
    MAX_PRICE = 'max price'
