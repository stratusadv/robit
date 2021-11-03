import ast
from datetime import datetime, timedelta


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


    # work backwards!
    def get_next_datetime(self):
        now = datetime.now()

        minute = None
        hour = None
        day_of_month = None
        month = None
        day_of_week = None

        if self.day_of_week.function == 'every':
            day_of_week = now.weekday()

        if self.month.function == 'every':
            month = now.month

        if self.day_of_month.function == 'every':
            day_of_month = now.day

        if self.hour.function == 'every':
            hour = now.hour

        if self.minute.function == 'every':
            minute = now.minute + 1

        next_datetime = datetime.now() + timedelta(minutes=minute)

        print(f'{minute = } {hour = } { day_of_month = } { month = } { day_of_week = }')



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



