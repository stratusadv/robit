from datetime import datetime, timedelta

from robit.core.cron import Cron

CREATED_DATE_FORMAT = '%b %d, %Y %I:%M%p'


class Clock:
    def __init__(
            self,
            cron: str = '* * * * *',
            utc_offset: int = 0,
    ):
        self.cron = Cron(value=cron, utc_offset=utc_offset)

        self.utc_offset = utc_offset

        self.created_utc = datetime.utcnow()
        self.created_tz = datetime.utcnow() + timedelta(hours=utc_offset)

    def as_dict(self):
        return {
            'created': self.created_tz_verbose,
            'now': self.now_tz_verbose,
            'next_run_datetime': self.next_run_datetime_verbose,
        }

    @property
    def created_utc_verbose(self):
        return self.created_utc.strftime(CREATED_DATE_FORMAT)

    @property
    def created_tz_verbose(self):
        return self.created_tz.strftime(CREATED_DATE_FORMAT)

    @property
    def now_tz_verbose(self):
        return (datetime.utcnow() + timedelta(hours=self.utc_offset)).strftime(CREATED_DATE_FORMAT)

    def is_past_next_run_datetime(self):
        if self.cron.is_past_next_datetime():
            return True
        else:
            return False

    @property
    def next_run_datetime_verbose(self):
        return self.cron.next_datetime.strftime(CREATED_DATE_FORMAT)
