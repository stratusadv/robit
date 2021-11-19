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

        cron_list = self.value.split(' ')

        if len(cron_list) != 5:
            raise ValueError(f'Cron string {self.value} is not the correct format. Should be 5 elements in a string "* * * * *"')

        self.minute = CronValue(cron_list[0])
        self.hour = CronValue(cron_list[1])
        self.day_of_month = CronValue(cron_list[2])
        self.month = CronValue(cron_list[3])
        self.day_of_week = CronValue(cron_list[4])

        self.next_datetime = None

        self.set_next_datetime()

    def as_dict(self):
        return {
            'next_run_datetime': self.next_run_datetime_verbose,
        }

    def is_past_next_datetime(self):
        if (datetime.utcnow().replace(second=0, microsecond=0) + timedelta(hours=self.utc_offset)) >= self.next_datetime:
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
        ndt = datetime.utcnow().replace(second=0, microsecond=0) + timedelta(hours=self.utc_offset)
        now = datetime.utcnow().replace(second=0, microsecond=0) + timedelta(hours=self.utc_offset)

        # Minute

        if self.minute.function == 'every':
            ndt += timedelta(minutes=1)
        elif self.minute.function == 'specific':
            ndt = ndt.replace(minute=self.minute.specific)

            if now.minute >= ndt.minute:
                ndt += timedelta(hours=1)
        elif self.minute.function == 'step':
            count_step_list = [0]
            count = self.minute.step
            while count < 60:
                count_step_list.append(count)
                count += self.minute.step

            for count_step in count_step_list:
                if count_step > now.minute:
                    ndt = ndt.replace(minute=count_step)
                    break
            else:
                ndt = ndt.replace(minute=0)
                ndt += timedelta(hours=1)

        # Hour

        if self.hour.function == 'every':
            pass

        if self.hour.function == 'specific':
            ndt = ndt.replace(hour=self.hour.specific)

            if ndt.hour == self.hour.specific:               
                if self.minute.function == 'specific':
                    if now.minute >= ndt.minute:
                        ndt += timedelta(days=1)

            if ndt.hour > self.hour.specific:
                ndt += timedelta(days=1)

        elif self.hour.function == 'step':
            count_step_list = [0]
            count = self.hour.step
            while count < 24:
                count_step_list.append(count)
                count += self.hour.step

            for count_step in count_step_list:
                if count_step > now.hour:
                    ndt = ndt.replace(hour=count_step)
                    break
            else:
                ndt = ndt.replace(hour=0)
                ndt += timedelta(days=1)

        # Day of Month

        if self.day_of_month.function == 'every':
            pass

        elif self.day_of_month.function == 'specific':
            ndt = ndt.replace(day=self.day_of_month.specific)

            if ndt.month == 12:
                next_month = 1
            else:
                next_month = ndt.month + 1

            if ndt.day == self.day_of_month.specific:

                if self.hour.function == 'specific':
                    if now.hour >= ndt.hour:
                        ndt = ndt.replace(month=next_month)

            if ndt.day > self.day_of_month.specific:
                ndt = ndt.replace(month=next_month)

        # Month

        if self.month.function == 'every':
            pass

        elif self.month.function == 'specific':
            ndt = ndt.replace(month=self.month.specific)

            if ndt.month == self.month.specific:

                if self.day_of_month.function == 'specific':
                    if now.day >= ndt.day:
                        ndt = ndt.replace(year=(ndt.year + 1))

            if now.month > ndt.month:
                ndt = ndt.replace(year=(ndt.year + 1))

        # Day of Week

        if self.day_of_week.function == 'every':
            pass

        if self.day_of_week.function == 'specific':
            if self.day_of_week.specific == 0:
                self.day_of_week.specific = 7

            if ndt.isoweekday() == self.day_of_week.specific:
                pass
                # print(f'{now.isoweekday() = } {ndt.isoweekday() = } {self.day_of_week.specific = }')
                # if self.hour.function == 'specific':
                #     if now.hour >= ndt.hour:
                #         ndt += timedelta(days=7)

            elif ndt.isoweekday() > self.day_of_week.specific:
                ndt += timedelta(days=(7 - (ndt.isoweekday() - self.day_of_week.specific)))

            else:
                ndt += timedelta(days=(self.day_of_week.specific - ndt.isoweekday()))

        self.next_datetime = ndt


class CronValue:
    def __init__(self, value: str, ):
        self.value = value

        FUNCTION_CHOICES = ('every', 'specific', 'range', 'step')

        self.function = None

        self.specific = None

        self.range_start = None
        self.range_stop = None

        self.step_start = None
        self.step = None

        self.process()

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



