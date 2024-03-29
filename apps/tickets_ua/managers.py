from datetime import timedelta

from django.db import models


class BaseParameterManager(models.Manager):
    def get_models_in_range(self, from_id, to_id, start_date, end_date, time_at):
        if not from_id or not to_id or not start_date or not end_date or not time_at:
            raise ValueError("The all params must be set.")

        if start_date > end_date:
            raise ValueError("The end date must be greater (or equal) than the start date.")

        current_date = start_date
        instances = []
        while current_date <= end_date:
            instance = self.model(
                from_station_id=from_id,
                to_station_id=to_id,
                time_at=time_at,
                date_at=current_date,
            )
            instances.append(instance)
            current_date += timedelta(days=1)

        return instances
