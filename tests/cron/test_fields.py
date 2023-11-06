import unittest
from datetime import datetime

from robit.cron.fields import CronSecondField, CronMinuteField, CronHourField, CronDayOfMonthField, CronMonthField, CronDayOfWeekField


class TestCronSecondField(unittest.TestCase):
    def setUp(self) -> None:
        self.second_cron = CronSecondField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 10)

    def test_minute_field(self):
        self.assertEqual(self.second_cron.increment_datetime(self.test_dt), datetime(2023, 7, 17, 4, 30, 11))


class TestCronMinuteField(unittest.TestCase):
    def setUp(self) -> None:
        self.minute_cron = CronMinuteField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 0)

    def test_minute_field(self):
        self.assertEqual(self.minute_cron.increment_datetime(self.test_dt), datetime(2023, 7, 17, 4, 31, 0))


class TestCronHourField(unittest.TestCase):
    def setUp(self) -> None:
        self.hour_cron = CronHourField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 0)

    def test_hour_field(self):
        self.assertEqual(self.hour_cron.increment_datetime(self.test_dt), datetime(2023, 7, 17, 5, 30, 0))


class TestCronDayOfMonthField(unittest.TestCase):
    def setUp(self) -> None:
        self.day_of_month_cron = CronDayOfMonthField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 0)

    def test_day_of_month_field(self):
        self.assertEqual(self.day_of_month_cron.increment_datetime(self.test_dt), datetime(2023, 7, 18, 4, 30, 0))


class TestCronMonthField(unittest.TestCase):
    def setUp(self) -> None:
        self.month_cron = CronMonthField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 0)

    def test_month_field(self):
        # Sets next month and back to day one to keep incrementing dates.
        self.assertEqual(self.month_cron.increment_datetime(self.test_dt), datetime(2023, 8, 1, 4, 30, 0))


class TestCronDayOfWeekField(unittest.TestCase):
    def setUp(self) -> None:
        self.day_of_week_cron = CronDayOfWeekField('*')
        self.test_dt = datetime(2023, 7, 17, 4, 30, 0)

    def test_day_of_week_field(self):
        self.assertEqual(self.day_of_week_cron.increment_datetime(self.test_dt), datetime(2023, 7, 18, 4, 30, 0))
