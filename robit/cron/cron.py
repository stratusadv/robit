from datetime import datetime

from robit.cron.fields import CronMinuteField, CronHourField, CronDayOfMonthField, CronMonthField, CronDayOfWeekField


class Cron:
    def __init__(self, cron_string):
        self.cron_string: str = cron_string
        self.field_dict: dict = self._parse_cron_field()

    def _parse_cron_field(self) -> dict:
        fields = self.cron_string.split()

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
        now = datetime.now()
        next_dt = now.replace(second=0, microsecond=0)

        # Todo: Need to validate it is looking for an actual date or catch the exception.
        while True:
            # Loop through each field and increment the datetime until the next valid datetime is found.
            for key, cron_field in self.field_dict.items():
                if not cron_field.is_valid_dt(next_dt):
                    next_dt = cron_field.increment_datetime(next_dt)
                    break
            else:
                # Else runs when loop completes without a break.
                # Once all fields are valid, check if the datetime is greater than the current datetime.
                if next_dt > now:
                    return next_dt
                else:
                    # Increment the minute field and try again.
                    next_dt = self.field_dict['minute'].increment_datetime(next_dt)
