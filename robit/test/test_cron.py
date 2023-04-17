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
        self.cron_every_second = cron.CronSpecificSecondField('30', start_datetime=self.start_datetime)

    def test_second_cron_next_value(self):
        self.assertEqual(self.cron_every_second.next_value(), 30)

    def test_cron_value_range(self):
        with self.assertRaises(ValueError):
            print('testing range')
            second_cron = cron.CronSpecificSecondField('60', self.start_datetime)
        with self.assertRaises(ValueError):
            second_cron = cron.CronSpecificSecondField('-50', self.start_datetime)

    def test_cron_value_error(self):
        with self.assertRaises(ValueError):
            second_cron = cron.CronSpecificSecondField('asdf', self.start_datetime)


if __name__ == '__main__':
    unittest.main()
