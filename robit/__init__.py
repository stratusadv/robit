import logging

from robit.worker.worker import Worker
from robit.config import config as _config

import pytz


def set_time_zone(timezone: str) -> None:
    if timezone in pytz.all_timezones_set:
        _config.TIMEZONE = timezone
    else:
        raise ValueError(f'"{timezone}" is an invalid time zone. Choices are {pytz.all_timezones_set}')


logging.basicConfig(
    format='Process - - [%(asctime)-15s] %(message)s -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

