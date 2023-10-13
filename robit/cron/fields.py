import calendar
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import Optional

from robit.cron.utils import CronFieldIdentifier, CronRangeFinder
from robit.cron.enums import CronFieldTypeEnum


class CronField(ABC):
    """
        Range creates a sequence of numbers starting at the first but does not include the last.
    """
    value_range: range = range(1, 60)

    def __init__(self, value: str) -> None:
        self.value = value
        self.type: CronFieldTypeEnum = self._get_type()
        self.possible_values: list = self._get_possible_values()

        if len(self.possible_values) == 0:
            raise ValueError(f'{self.value} is not a valid cron field pattern.')

    def _get_possible_values(self) -> list:
        range_finder = CronRangeFinder(self)
        return range_finder.possible_values()

    @abstractmethod
    def increment_datetime(self, dt: datetime) -> datetime:
        pass

    @abstractmethod
    def is_valid_dt(self, dt: datetime) -> bool:
        pass

    def _get_type(self) -> CronFieldTypeEnum:
        return CronFieldIdentifier(self.value).identify()


class CronSecondField(CronField):
    value_range: range = range(0, 60)

    def increment_datetime(self, dt: datetime) -> datetime:
        return dt + timedelta(seconds=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.second in self.possible_values


class CronMinuteField(CronField):
    value_range: range = range(0, 60)

    def increment_datetime(self, dt: datetime) -> datetime:
        return dt + timedelta(minutes=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.minute in self.possible_values


class CronHourField(CronField):
    value_range: range = range(0, 24)

    def increment_datetime(self, dt: datetime) -> datetime:
        return dt + timedelta(hours=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.hour in self.possible_values


class CronDayOfMonthField(CronField):
    value_range: range = range(1, 32)
    _current_month: Optional[int] = None

    def increment_datetime(self, dt: datetime) -> datetime:
        return dt + timedelta(days=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.day in self.possible_values


class CronMonthField(CronField):
    value_range: range = range(1, 13)

    def increment_datetime(self, dt: datetime) -> datetime:
        # Sets next month and back to day one to keep incrementing dates.
        if dt.month == 12:
            return dt.replace(year=dt.year + 1, month=1, day=1)
        else:
            return dt.replace(month=dt.month + 1, day=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.month in self.possible_values


class CronDayOfWeekField(CronField):
    value_range: range = range(0, 7)

    def increment_datetime(self, dt: datetime) -> datetime:
        return dt + timedelta(days=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        cron_day_of_week = (dt.weekday() + 1) % 7
        return cron_day_of_week in self.possible_values
