import ast
from datetime import datetime, timedelta
import calendar
from robit.core.clock import CREATED_DATE_FORMAT


class Cron:
    def __init__(
            self,
            value: str,
            utc_offset: int = 0,
    ):
        self.value = value
        self.utc_offset = utc_offset

        cron_segment_list = self.value.split(' ')
        if 5 > len(cron_segment_list) > 6:
            value_error = f'Cron string {self.value} is not the correct length.\n'
            value_error += f'Should be 5 elements in a string "* * * * *"]\n'
            value_error += f'or 6 elements in a string if your working with seconds "* * * * * *"'
            raise ValueError(value_error)

        if len(cron_segment_list) == 6:
            self.second = SecondCronValue(cron_segment_list[0])
            cron_segment = 1
        else:
            cron_segment = 0
            self.second = SecondCronValue('00')

        self.minute = MinuteCronValue(cron_segment_list[cron_segment])
        self.hour = HourCronValue(cron_segment_list[cron_segment + 1])
        self.day_of_month = DayOfMonthCronValue(cron_segment_list[cron_segment + 2])
        self.month = MonthCronValue(cron_segment_list[cron_segment + 3])
        self.day_of_week = DayOfWeekCronValue(cron_segment_list[cron_segment + 4])

        self.next_datetime = None

        self.set_next_datetime()

    def as_dict(self):
        return {
            'next_run_datetime': self.next_run_datetime_verbose,
        }

    def is_past_a_datetime(self, a_datetime):
        if a_datetime >= self.next_datetime:
            return True
        else:
            return False

    def is_past_next_datetime(self):
        if self.is_past_a_datetime((datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset))):
            self.set_next_datetime()
            return True
        else:
            return False

    def is_past_next_run_datetime(self):
        if self.is_past_next_datetime():
            return True
        else:
            return False

    @property
    def next_run_datetime_verbose(self):
        return self.next_datetime.strftime(CREATED_DATE_FORMAT)

    def set_next_datetime(self):
        ndt = datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset)
        now = datetime.utcnow().replace(microsecond=0) + timedelta(hours=self.utc_offset)

        ndt = self.second.get_next_date_time(ndt, now)
        ndt = self.minute.get_next_date_time(ndt, now, second=self.second)
        ndt = self.hour.get_next_date_time(ndt, now, minute=self.minute)
        ndt = self.day_of_month.get_next_date_time(ndt, now, hour=self.hour)
        ndt = self.month.get_next_date_time(ndt, now, day_of_month=self.day_of_month)
        ndt = self.day_of_week.get_next_date_time(ndt, now)

        self.next_datetime = ndt


class CronValue:
    def __init__(self, value: str, ):
        self.value = value

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


class SecondCronValue(CronValue):
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


class MinuteCronValue(CronValue):
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


class HourCronValue(CronValue):
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


class DayOfMonthCronValue(CronValue):
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


class MonthCronValue(CronValue):
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


class DayOfWeekCronValue(CronValue):
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
