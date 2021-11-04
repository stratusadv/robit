import ast
from datetime import datetime, timedelta
import calendar


class Cron:
    def __init__(self, value: str):
        self.value = value

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


    def is_past_next_datetime(self):
        if datetime.now().replace(second=0, microsecond=0) >= self.next_datetime:
            self.set_next_datetime()
            return True
        else:
            return False

    def set_next_datetime(self):
        ndt = datetime.now().replace(second=0, microsecond=0)
        now = datetime.now().replace(second=0, microsecond=0)

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

        if self.hour.function == 'specific':

            if ndt.hour == self.hour.specific:               
                if self.minute.function == 'specific':
                    if ndt.minute >= self.minute.specific:
                        ndt += timedelta(days=1)
                        
            if ndt.hour > self.hour.specific:
                ndt += timedelta(days=1)


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
            if range_list[0] == '*':
                self.function = 'every'
            elif isinstance(ast.literal_eval(range_list[0]), int):
                self.function = 'specific'
                self.specific = int(range_list[0])



