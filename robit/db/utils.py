from datetime import datetime

ISO8601_FORMAT = '%Y-%m-%d %H:%M:%S'


def datetime_to_string(dt: datetime ) -> str:
    return dt.strftime(ISO8601_FORMAT)


def string_to_datetime(datetime_string: str) -> datetime:
    return datetime.now().strptime(datetime_string, ISO8601_FORMAT)