import logging
from logging.handlers import TimedRotatingFileHandler

from robit.worker.worker import Worker
from robit.config import config as _config

import pytz


def set_database_file_name(name: str) -> None:
    _config.DATABASE_FILE_NAME = name


def set_log_file_name(name: str) -> None:
    _config.LOG_FILE_NAME = name


def set_log_backup_days(days: int) -> None:
    _config.LOG_BACKUP_DAYS = days


def set_time_zone(timezone: str) -> None:
    if timezone in pytz.all_timezones_set:
        _config.TIMEZONE = timezone
    else:
        raise ValueError(f'"{timezone}" is an invalid time zone. Choices are {pytz.all_timezones_set}')


timed_rotating_log_handler = TimedRotatingFileHandler(
    _config.LOG_FILE_NAME,
    when='midnight',
    backupCount=_config.LOG_BACKUP_DAYS,
)
timed_rotating_log_handler.setLevel(logging.WARNING)

stream_log_handler = logging.StreamHandler()
stream_log_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format='Process - %(levelname)s - [%(asctime)-15s] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    handlers=[
        timed_rotating_log_handler,
        stream_log_handler,
    ]
)

