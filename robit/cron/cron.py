from datetime import datetime

from robit.cron.fields import CronSecondField, CronMinuteField, CronHourField, CronDayOfMonthField, CronMonthField, CronDayOfWeekField
from robit.core.clock import CREATED_DATE_FORMAT, Clock


class Cron:
    def __init__(self, cron_syntax: str) -> None:
        """
        Responsible for parsing a cron string and returning the next datetime that the cron string will run.
        """
        self.cron_syntax = cron_syntax
        self.field_dict: dict = self._parse_cron_field()
        self.clock = Clock()

    def _parse_cron_field(self) -> dict:
        fields = self.cron_syntax.split()
        field_length = len(fields)

        if field_length not in [5, 6]:
            raise ValueError('Invalid cron string format')

        if field_length == 5:
            fields[:0] = '0'

        return {
            'second': CronSecondField(fields[0]),
            'minute': CronMinuteField(fields[1]),
            'hour': CronHourField(fields[2]),
            'day_of_month': CronDayOfMonthField(fields[3]),
            'month': CronMonthField(fields[4]),
            'day_of_week': CronDayOfWeekField(fields[5])
        }

    def next_datetime(self) -> datetime:
        now = self.clock.now_tz
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
                    next_dt = self.field_dict['second'].increment_datetime(next_dt)

    def next_datetime_verbose(self) -> str:
        return self.next_datetime().strftime(CREATED_DATE_FORMAT)