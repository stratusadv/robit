from datetime import datetime, timedelta

CREATED_DATE_FORMAT = '%b %d, %Y %I:%M%p'


class Clock:
    def __init__(
            self,
            utc_offset: int = 0,
    ):

        self.utc_offset = utc_offset

        self.created_utc = datetime.utcnow()
        self.created_tz = datetime.utcnow() + timedelta(hours=utc_offset)

    def as_dict(self):
        return {
            'created': self.created_tz_verbose,
            'now': self.now_tz_verbose,
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

