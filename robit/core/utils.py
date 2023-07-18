from datetime import datetime, timedelta
from robit.config import config


def tz_now() -> datetime:
    return (datetime.utcnow() + timedelta(hours=config.UTC_OFFSET)).replace(microsecond=0)
