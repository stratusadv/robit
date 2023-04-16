import ast
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import calendar
from robit.core.clock import CREATED_DATE_FORMAT


class Cron:
    def __init__(
            self,
            cron_syntax: str,
            utc_offset: int = 0,
    ):
        self.cron_syntax = self.set_cron_syntax(cron_syntax)
        self.utc_offset = utc_offset

        cron_segment_list = self.cron_syntax.split(' ')

        if len(cron_segment_list) == 6:
            self.second = SecondCronField(cron_segment_list[0])
            cron_segment = 1
        else:
            cron_segment = 0
            self.second = SecondCronField('00')

        self.minute = MinuteCronField(cron_segment_list[cron_segment])
        self.hour = HourCronField(cron_segment_list[cron_segment + 1])
        self.day_of_month = DayOfMonthCronField(cron_segment_list[cron_segment + 2])
        self.month = MonthCronField(cron_segment_list[cron_segment + 3])
        self.day_of_week = DayOfWeekCronField(cron_segment_list[cron_segment + 4])

        self.next_run_datetime = None

        self.set_next_run_time()

    def as_dict(self):
        return {
            'next_run_datetime': self.next_run_datetime_verbose,
        }

    def is_past_a_datetime(self, a_datetime):
        return a_datetime >= self.next_run_datetime

    def is_past_next_run_datetime(self):
        return self.now() >= self.next_run_datetime

    @property
    def next_run_datetime_verbose(self):
        return self.next_run_datetime.strftime(CREATED_DATE_FORMAT)

    def now(self):
        return datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset)

    def set_cron_syntax(self, cron_syntax):
        cron_segment_list = cron_syntax.split(' ')
        if len(cron_segment_list) < 5 or len(cron_segment_list) > 6:
            raise ValueError(f'Cron syntax must by 5 or 6 values in the format "* * * * * *"')

        if cron_syntax == 5:
            cron_segment_list = ['00'] + cron_segment_list
        self.cron_syntax = " ".join(cron_segment_list)
        return " ".join(cron_segment_list)

    def set_next_run_time(self):
        ndt = datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset)
        now = datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset)

        ndt = self.second.get_next_date_time(ndt, now)
        ndt = self.minute.get_next_date_time(ndt, now, second=self.second)
        ndt = self.hour.get_next_date_time(ndt, now, minute=self.minute)
        ndt = self.day_of_month.get_next_date_time(ndt, now, hour=self.hour)
        ndt = self.month.get_next_date_time(ndt, now, day_of_month=self.day_of_month)
        ndt = self.day_of_week.get_next_date_time(ndt, now)

        self.next_run_datetime = ndt


class CronField:
    def __init__(self, field: str, ):
        self.value = field

        self.function = None

        self.specific = None

        self.range_start = None
        self.range_stop = None

        self.step_start = None
        self.step = None

        self.process()

    def get_next_date_time(self, ndt, now, **kwargs):
        pass

    def process(self):
        range_list = self.value.split('-')

        value_error = 'Invalid cron string used.'

        if len(range_list) == 2:
            self.function = 'range'
            self.range_start = int(range_list[0])
            self.range_stop = int(range_list[1])
        elif len(step_list := self.value.split('/')) == 2:
            if step_list[0] == '*':
                self.function = 'step'
                self.step_start = step_list[0]
                self.step = int(step_list[1])
            else:
                raise ValueError(value_error)
        else:
            if range_list[0] == '*':
                self.function = 'every'
            elif isinstance(ast.literal_eval(range_list[0]), int):
                self.function = 'specific'
                self.specific = int(range_list[0])
            else:
                raise ValueError(value_error)


class CronAnyField(ABC):
    def __init__(self, value: str, start_datetime: datetime):
        self.value = value
        self.start_datetime = start_datetime

    def check_range(self, value_range):
        value_error = 'Value not in range'
        if int(self.value) not in range:
            raise ValueError(value_error)

    def check_value_type(self):
        if self.value == '*':
            return True

        try:
            value_int = int(self.value)
            return True
        except ValueError:
            raise ValueError('Value must be * or a string that can be converted to int in range.')

    @abstractmethod
    def validate_value(self):
        pass

    @abstractmethod
    def next_value(self):
        pass


class CronAnySecondField(CronAnyField):
    def next_value(self):
        return (self.start_datetime + timedelta(seconds=int(self.value))).second

    def validate_value(self) -> None:
        self.check_value_type()
        self.check_range(range(1, 59))


class CronAnyMinuteField(CronAnySecondField):
    def next_value(self):
        """
            Returns the next minute the cron is scheduled.
        """
        return (self.start_datetime + timedelta(minutes=self.value)).minute

    def set_value(self, value) -> int:
        value_error = 'Field value must be between 0-59 minutes'
        try:
            value_int = int(value)
        except ValueError:
            raise ValueError(value_error)

        if value_int < 0 or value_int > 59:
            raise ValueError(value_error)
        return value_int


class CronAnyHourField(CronAnySecondField):
    def next_value(self):
        """
            Returns the next hour the cron is scheduled.
        """
        return (self.start_datetime + timedelta(hours=self.value)).hour

    def set_value(self, value) -> int:
        value_error = 'Field value must be between 0-23 hours'
        try:
            value_int = int(value)
        except ValueError:
            raise ValueError(value_error)

        if value_int < 0 or value_int > 23:
            raise ValueError(value_error)
        return value_int


class CronAnyDayField(CronAnySecondField):
    def next_value(self):
        """
            Returns the next month the cron is scheduled for.
            Check to see if day has passed in current month.
            Find next month that has that day number.
        """

        return (self.start_datetime + timedelta(minutes=self.value)).minute

    def set_value(self, value) -> int:
        value_error = 'Field value must be between 1-31 days'
        try:
            value_int = int(value)
        except ValueError:
            raise ValueError(value_error)

        if value_int < 1 or value_int >= 31:
            raise ValueError(value_error)
        return value_int



class CronMultipleField(CronField):
    pass


class CronRangeField(CronField):
    pass


class CronStepField(CronField):
    pass


class SecondCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            ndt += timedelta(seconds=1)
        elif self.function == 'specific':
            ndt = ndt.replace(second=self.specific)

            if now.second >= self.specific:
                ndt += timedelta(minutes=1)

        elif self.function == 'step':
            count_step_list = [0]
            count = self.step
            while count < 60:
                count_step_list.append(count)
                count += self.step

            for count_step in count_step_list:
                if count_step > now.minute:
                    ndt = ndt.replace(second=count_step)
                    break
            else:
                ndt = ndt.replace(second=0)
                ndt += timedelta(minutes=1)

        return ndt


class MinuteCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            pass
        elif self.function == 'specific':
            ndt = ndt.replace(minute=self.specific)
            # if kwargs['second'].function == 'specific':
            #     if now.second >= ndt.second:
            #         ndt += timedelta(minutes=1)

            if now.minute >= self.specific:
                ndt += timedelta(hours=1)

        elif self.function == 'step':
            count_step_list = [0]
            count = self.step
            while count < 60:
                count_step_list.append(count)
                count += self.step

            for count_step in count_step_list:
                if count_step > now.minute:
                    ndt = ndt.replace(minute=count_step)
                    break
            else:
                ndt = ndt.replace(minute=0)
                ndt += timedelta(hours=1)

        return ndt


class HourCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            pass

        if self.function == 'specific':
            ndt = ndt.replace(hour=self.specific)

            # if ndt.hour == self.specific:
            #     if kwargs['minute'].function == 'specific':
            #         if now.minute >= ndt.minute:
            #             ndt += timedelta(days=1)

            if now.hour >= self.specific:
                ndt += timedelta(days=1)

        elif self.function == 'step':
            count_step_list = [0]
            count = self.step
            while count < 24:
                count_step_list.append(count)
                count += self.step

            for count_step in count_step_list:
                if count_step > now.hour:
                    ndt = ndt.replace(hour=count_step)
                    break
            else:
                ndt = ndt.replace(hour=0)
                ndt += timedelta(days=1)

        return ndt


class DayOfMonthCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            pass

        elif self.function == 'specific':
            ndt = ndt.replace(day=self.specific)

            if ndt.month == 12:
                next_month = 1
            else:
                next_month = ndt.month + 1

            if ndt.day == self.specific:

                if kwargs['hour'].function == 'specific':
                    if now.hour >= ndt.hour:
                        ndt = ndt.replace(month=next_month)

            if now.day > self.specific:
                ndt = ndt.replace(month=next_month)

        return ndt


class MonthCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            pass

        elif self.function == 'specific':
            ndt = ndt.replace(month=self.specific)

            if ndt.month == self.specific:

                if kwargs['day_of_month'].function == 'specific':
                    if now.day >= ndt.day:
                        ndt = ndt.replace(year=(ndt.year + 1))

            if now.month > ndt.month:
                ndt = ndt.replace(year=(ndt.year + 1))

        return ndt


class DayOfWeekCronField(CronField):
    def get_next_date_time(self, ndt: datetime, now: datetime, **kwargs) -> datetime:
        if self.function == 'every':
            pass

        if self.function == 'specific':
            if self.specific == 0:
                self.specific = 7

            if ndt.isoweekday() == self.specific:
                pass
                # print(f'{now.isoweekday() = } {ndt.isoweekday() = } {self.specific = }')
                # if self.hour.function == 'specific':
                #     if now.hour >= ndt.hour:
                #         ndt += timedelta(days=7)

            elif ndt.isoweekday() > self.specific:
                ndt += timedelta(days=(7 - (ndt.isoweekday() - self.specific)))

            else:
                ndt += timedelta(days=(self.specific - ndt.isoweekday()))

        return ndt
