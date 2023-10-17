from datetime import datetime, timedelta

from robit.config import config

import pytz

CREATED_DATE_FORMAT = '%b %d, %Y at %I:%M:%S %p'


class Clock:
    def __init__(self) -> None:
        self.created_utc = datetime.utcnow()
        self.created_tz = self.now_tz

    def as_dict(self) -> dict:
        return {
            'created': self.created_tz_verbose,
            'now': self.now_tz_verbose,
        }

    @property
    def created_utc_verbose(self) -> str:
        return self.created_utc.strftime(CREATED_DATE_FORMAT)

    @property
    def created_tz_verbose(self) -> str:
        return self.created_tz.strftime(CREATED_DATE_FORMAT)

    @property
    def now_tz(self) -> datetime:
        return datetime.now(pytz.timezone(config.TIMEZONE)).replace(microsecond=0)

    @property
    def now_tz_verbose(self) -> str:
        return self.now_tz.strftime(CREATED_DATE_FORMAT)

