from abc import ABC, abstractmethod
from datetime import datetime, timedelta

from robit.cron.utils import CronFieldIdentifier, CronRangeFinder
from robit.cron.enums import CronFieldTypeEnum


class CronField(ABC):
    value_range: range = range(1, 59)

    def __init__(self, value):
        self.value = value
        self.possible_values: list = self._get_possible_values()
        self.type: CronFieldTypeEnum = self._get_type()

    def _get_possible_values(self) -> list:
        range_finder = CronRangeFinder(self)
        return range_finder.possible_values()

    @abstractmethod
    def increment_datetime(self, dt) -> datetime:
        pass

    @abstractmethod
    def is_valid_dt(self, dt: datetime) -> bool:
        pass

    def _get_type(self):
        return CronFieldIdentifier(self).identify()


class CronMinuteField(CronField):
    value_range: range = range(0, 59)

    def increment_datetime(self, dt) -> datetime:
        return dt + timedelta(minutes=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.minute in self.possible_values


class CronHourField(CronField):
    value_range: range = range(0, 23)

    def increment_datetime(self, dt) -> datetime:
        return dt + timedelta(hours=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.hour in self.possible_values


class CronDayOfMonthField(CronField):
    value_range: range = range(1, 31)

    def increment_datetime(self, dt) -> datetime:
        return dt + timedelta(days=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.day in self.possible_values


class CronMonthField(CronField):
    value_range: range = range(1, 12)

    def increment_datetime(self, dt) -> datetime:
        return dt.replace(month=dt.month % 12 + 1, day=1) + timedelta(days=(dt.day == 1) - 1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.month in self.possible_values


class CronDayOfWeekField(CronField):
    value_range: range = range(0, 6)

    def increment_datetime(self, dt) -> datetime:
        return dt + timedelta(days=1)

    def is_valid_dt(self, dt: datetime) -> bool:
        return dt.weekday() in self.possible_values
