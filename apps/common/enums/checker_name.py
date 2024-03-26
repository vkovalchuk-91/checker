from enum import Enum


class CheckerTypeName(Enum):
    HOTLINE_UA = 'hotline_ua'
    TICKETS_UA = 'tickets_ua'

    @staticmethod
    def find_by_value(value):
        if not value:
            return None

        for task_name in CheckerTypeName:
            if task_name.value == value:
                return task_name

        return None
