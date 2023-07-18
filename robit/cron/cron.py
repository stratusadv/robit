from datetime import datetime, timedelta

from robit.core.utils import tz_now
from robit.cron.fields import CronMinuteField, CronHourField, CronDayOfMonthField, CronMonthField, CronDayOfWeekField
from robit.core.clock import CREATED_DATE_FORMAT
from robit.config import config


class Cron:
    def __init__(self, cron_syntax: str):
        """
        Responsible for parsing a cron string and returning the next datetime that the cron string will run.
        """
        self.cron_syntax = cron_syntax
        self.field_dict: dict = self._parse_cron_field()

    def _parse_cron_field(self) -> dict:
        fields = self.cron_syntax.split()

        if len(fields) != 5:
            raise ValueError("Invalid cron string format")

        return {
            "minute": CronMinuteField(fields[0]),
            "hour": CronHourField(fields[1]),
            "day_of_month": CronDayOfMonthField(fields[2]),
            "month": CronMonthField(fields[3]),
            "day_of_week": CronDayOfWeekField(fields[4])
        }

    def next_datetime(self) -> datetime:
        now = tz_now()
        next_dt = now.replace(second=0, microsecond=0)

        while True:
            # Loop through each field and increment the datetime until the next valid datetime is found.
            for key, cron_field in self.field_dict.items():
                if not cron_field.is_valid_dt(next_dt):
                    next_dt = cron_field.increment_datetime(next_dt)
                    break
                elif next_dt.year - now.year > 4:
                    raise ValueError("Cron string is invalid")
            else:
                # Else runs when loop completes without a break.
                # Once all fields are valid, check if the datetime is greater than the current datetime.
                if next_dt > now:
                    return next_dt
                else:
                    # Increment the minute field and try again.
                    next_dt = self.field_dict['minute'].increment_datetime(next_dt)

    def next_datetime_verbose(self) -> str:
        return self.next_datetime().strftime(CREATED_DATE_FORMAT)