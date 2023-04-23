import re
from abc import ABC, abstractmethod
from datetime import datetime, timedelta


class Cron:
    def __init__(self, cron_string):
        self.cron_string = cron_string
        self.field_dict = self._parse_cron_field()

    def _parse_cron_field(self) -> dict:
        fields = self.cron_string.split()

        if len(fields) != 5:
            raise ValueError("Invalid cron string format")

        return {
            "minute": CronMinuteField(fields[0]),
            "hour": CronHourField(fields[1]),
            "day_of_month": CronDayOfMonthField(fields[2]),
            "month": CronMonthField(fields[3]),
            "day_of_week": CronDayOfWeekField(fields[4])
        }

    def next_datetime(self) -> datetime:
        now = datetime.now()
        next_dt = now.replace(second=0, microsecond=0)

        while True:
            """
                Loop through each field and increment the datetime until the next valid datetime is found.
            """
            for key, cron_field in self.field_dict.items():
                if not cron_field.is_valid_dt(next_dt):
                    next_dt = cron_field.increment_datetime(next_dt)
                    break
            else:
                """
                 Once all fields are valid, check if the datetime is greater than the current datetime.
                """
                if next_dt > now:
                    return next_dt
                else:
                    """
                        If the datetime is not greater than the current datetime, increment the minute field and try again.
                    """
                    next_dt = self.field_dict['minute'].increment_datetime(next_dt)


class CronField(ABC):
    value_range: range = range(1, 59)

    def __init__(self, value):
        self.value = value
        self.possible_values = self._get_possible_values()
        # self._validate()

    def _get_possible_values(self) -> list:
        range_finder = CronRangeFinder(self)
        return range_finder.value_range()

    @abstractmethod
    def increment_datetime(self, dt) -> datetime:
        pass

    @abstractmethod
    def is_valid_dt(self, dt: datetime) -> bool:
        pass

    # Todo: validate values
    def type(self):
        return CronIdentifier(self).identify()


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


class CronIdentifier:
    def __init__(self, cron_field: CronField):
        self.cron_field: CronField = cron_field
        self._identifiers = [self._is_every, self._is_range, self._is_step, self._is_list, self._is_specific]

    def identify(self):
        for identifier in self._identifiers:
            if identifier():
                return identifier.__name__.split('_')[-1]

        raise ValueError('Invalid cron string used.')

    def _is_every(self):
        return self.cron_field.value == '*'

    def _is_range(self):
        pattern = r'^\d+-\d+$'
        return bool(re.match(pattern, self.cron_field.value))

    def _is_step(self):
        return '/' in self.cron_field.value

    def _is_list(self):
        return ',' in self.cron_field.value

    def _is_specific(self):
        pattern = re.compile(r'^\d+$')
        return bool(pattern.match(self.cron_field.value))


class CronRangeFinder:
    # Todo all range error checking should be in cron field.
    def __init__(self, cron_field: CronField):
        self.cron_field = cron_field
        self.possible_values = []

    def value_range(self):
        self.possible_values = []
        cron_type = self.cron_field.type()
        if cron_type == 'every':
            self._every()
        elif cron_type == 'specific':
            self._specific()
        elif cron_type == 'step':
            self._step()
        elif cron_type == 'list':
            self._list()
        elif cron_type == 'range':
            self._range()

        return [int(value) for value in self.possible_values]

    def _every(self):
        self.possible_values = list(range(self.cron_field.value_range.start, self.cron_field.value_range.stop + 1))

    def _specific(self):
        if int(self.cron_field.value) not in self.cron_field.value_range:
            raise ValueError(f'Value {self.cron_field.value} is not withing the range {self.cron_field.value_range}')

        self.possible_values.append(self.cron_field.value)

    def _step(self):
        cron_segment = self.cron_field.value.split('/')
        step_value = int(cron_segment[-1])
        cron_field_value = cron_segment[0]

        # Todo: Copy class instance and use it to get the possible values?
        # Todo: Better error handling

        temp_cron_field = CronMinuteField(cron_field_value)
        temp_cron_range_finder = CronRangeFinder(temp_cron_field)
        possible_values = temp_cron_range_finder.value_range()
        self.possible_values = possible_values[::step_value]

    def _list(self):
        for value in self.cron_field.value.split(','):
            if int(value) not in self.cron_field.value_range:
                raise ValueError(f'Value {value} is not withing the range {self.cron_field.value_range.start} to {self.cron_field.value_range.stop}.')
            self.possible_values.append(int(value))

    def _range(self):
        value_list = self.cron_field.value.split('-')
        start_value = int(value_list[0])
        end_value = int(value_list[1])

        if start_value not in self.cron_field.value_range:
            raise ValueError(
                f'Start value is not withing the range {self.cron_field.value_range.start} to {self.cron_field.value_range.stop}.')

        if end_value not in self.cron_field.value_range:
            raise ValueError(f'End value is not withing the range {self.cron_field.value_range.start} to {self.cron_field.value_range.stop}.')

        for value in range(int(start_value), int(end_value) + 1):
            self.possible_values.append(value)


cron = Cron('24 * * * *')
print(cron.next_datetime())
