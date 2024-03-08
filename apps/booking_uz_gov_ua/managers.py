from datetime import timedelta

from django.db import models
from django.db.models import Q


class CheckerManager(models.Manager):
    def create_checkers_in_range(self, from_station, to_station, start_date, end_date, time_at, user):
        if not from_station or not to_station or not start_date or not end_date or not time_at or not user:
            raise ValueError("The all params must be set.")

        if start_date > end_date:
            raise ValueError("The end date must be greater (or equal) than the start date.")

        current_date = start_date
        checkers = []
        while current_date <= end_date:
            checker = self.model(
                from_station=from_station,
                to_station=to_station,
                time_at=time_at,
                user=user,
                date_at=current_date,
            )

            if not self.is_exist(from_station=from_station, to_station=to_station, date_at=current_date, user=user):
                checkers.append(checker)

            current_date += timedelta(days=1)

        checkers = super().get_queryset().bulk_create(checkers)
        return checkers

    def is_exist(self, from_station, to_station, date_at, user):
        return super().get_queryset().filter(
            Q(from_station=from_station) &
            Q(to_station=to_station) &
            Q(date_at=date_at) &
            Q(user_id=user.id)
        ).exists()
