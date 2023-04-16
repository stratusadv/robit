import unittest
from datetime import datetime

from robit.core import cron


class TestCron(unittest.TestCase):
    def setUp(self) -> None:
        self.test_cron = cron.Cron('* 51 6 * * *')
        self.datetime_now = datetime.utcnow().replace(microsecond=0)

    def test_cron_value_length_error(self):
        with self.assertRaises(ValueError):
            cron.Cron('* * * * * * * *')

        with self.assertRaises(ValueError):
            cron.Cron('* *')

    def test_five_digit_cron_value_init(self):
        test_cron = cron.Cron('6 20 * * *')
        self.assertTrue(test_cron.second.value, '00')
        self.assertTrue(test_cron.minute.value, '6')
        self.assertTrue(test_cron.hour.value, '6')

    def test_six_digit_cron_value_init(self):
        test_cron = cron.Cron('20 * * * * *')
        self.assertTrue(test_cron.second.value, '20')

    def test_cron_time(self):
        self.assertFalse(
            self.test_cron.is_past_a_datetime(self.datetime_now),
        )


class CronAnySecondFieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_datetime = datetime.utcnow().replace(second=0)
        self.cron_every_second = cron.CronAnySecondField('30', start_datetime=self.start_datetime)

    def test_second_cron_next_value(self):
        self.assertEqual(self.cron_every_second.next_value(), 30)

    def test_cron_value_range(self):
        with self.assertRaises(ValueError):
            cron.CronAnySecondField('60', self.start_datetime)
        with self.assertRaises(ValueError):
            cron.CronAnySecondField('-50', self.start_datetime)

    def test_cron_value_error(self):
        with self.assertRaises(ValueError):
            cron.CronAnySecondField('asdf', self.start_datetime)


class CronAnyMinuteFieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_datetime = datetime.utcnow().replace(minute=59)
        self.cron_any_minute = cron.CronAnyMinuteField('5', start_datetime=self.start_datetime)

    def test_second_cron_next_value(self):
        self.assertEqual(self.cron_any_minute.next_value(), 4)

    def test_cron_value_range(self):
        with self.assertRaises(ValueError):
            cron.CronAnyMinuteField('60', self.start_datetime)
        with self.assertRaises(ValueError):
            cron.CronAnyMinuteField('-50', self.start_datetime)

    def test_cron_value_error(self):
        with self.assertRaises(ValueError):
            cron.CronAnyMinuteField('asdf', self.start_datetime)


class CronAnyHourFieldTest(unittest.TestCase):
    def setUp(self) -> None:
        self.start_datetime = datetime.utcnow().replace(hour=23)
        self.cron_any_hour = cron.CronAnyHourField('2', start_datetime=self.start_datetime)

    def test_second_cron_next_value(self):
        self.assertEqual(self.cron_any_hour.next_value(), 1)

    def test_cron_value_range(self):
        with self.assertRaises(ValueError):
            cron.CronAnyHourField('24', self.start_datetime)
        with self.assertRaises(ValueError):
            cron.CronAnyHourField('-1', self.start_datetime)

    def test_cron_value_error(self):
        with self.assertRaises(ValueError):
            cron.CronAnyHourField('asdf', self.start_datetime)


# class CronAnyDayFieldTest(unittest.TestCase):
#     def setUp(self) -> None:
#         self.start_datetime = datetime.utcnow().replace(day=1)
#         self.cron_any_day = cron.CronAnyDayField('3', start_datetime=self.start_datetime)
#
#     def test_second_cron_next_value(self):
#         self.assertEqual(self.cron_any_day.next_value(), 3)
#
#     def test_cron_value_range(self):
#         with self.assertRaises(ValueError):
#             cron.CronAnyDayField('32', self.start_datetime)
#         with self.assertRaises(ValueError):
#             cron.CronAnyDayField('0', self.start_datetime)
#
#     def test_cron_value_error(self):
#         with self.assertRaises(ValueError):
#             cron.CronAnyDayField('asdf', self.start_datetime)


if __name__ == '__main__':
    unittest.main()
