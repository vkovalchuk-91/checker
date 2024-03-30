from datetime import timedelta

from django.db import models

from apps.task_manager.models import CheckerTask


class BaseParameterManager(models.Manager):
    def get_models_in_range(self, from_id, to_id, start_date, end_date, time_at, user_id):
        if not from_id or not to_id or not start_date or not end_date or not time_at:
            raise ValueError("The all params must be set.")

        if start_date > end_date:
            raise ValueError("The end date must be greater (or equal) than the start date.")

        current_date = start_date
        instances = []

        while current_date <= end_date:
            instance = self.model(
                # param_type=param_type,
                from_station_id=from_id,
                to_station_id=to_id,
                time_at=time_at,
                date_at=current_date,
            )

            if not self._is_exist(
                    from_id=from_id,
                    to_id=to_id,
                    date_at=current_date,
                    time_at=time_at,
                    user_id=user_id
            ):
                instances.append(instance)

            current_date += timedelta(days=1)
        return instances

    def _is_exist(self, from_id, to_id, date_at, time_at, user_id):
        return CheckerTask.objects.filter(
            is_active=True,
            is_delete=False,
            task_param__ticket_ua_search_parameters__from_station_id=from_id,
            task_param__ticket_ua_search_parameters__to_station_id=to_id,
            task_param__ticket_ua_search_parameters__date_at=date_at,
            task_param__ticket_ua_search_parameters__time_at=time_at,
            user_id=user_id,
        ).exists()
