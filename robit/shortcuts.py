from robit.config import config as _config

import pytz as _pytz


def set_database_file_name(name: str) -> None:
    _config.DATABASE_FILE_NAME = name


def set_log_file_name(name: str) -> None:
    _config.LOG_FILE_NAME = name


def set_log_backup_days(days: int) -> None:
    _config.LOG_BACKUP_DAYS = days


def set_controls(status: bool) -> None:
    _config.CONTROLS = status


def set_database_logging(status: bool) -> None:
    _config.DATABASE_LOGGING = status


def set_timezone(timezone: str) -> None:
    if timezone in _pytz.all_timezones_set:
        _config.TIMEZONE = timezone
    else:
        raise ValueError(f'"{timezone}" is an invalid time zone. Choices are {_pytz.all_timezones_set}')
