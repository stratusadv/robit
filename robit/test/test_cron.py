import unittest
from datetime import datetime

from robit.core.cron import Cron


class TestCron(unittest.TestCase):
    def setUp(self) -> None:
        self.cron = Cron('* 51 6 * * *')
        self.datetime_now = datetime.utcnow().replace(microsecond=0)

    def test_cron_value_length_error(self):
        with self.assertRaises(ValueError):
            Cron('*')
        with self.assertRaises(ValueError):
            Cron('* * * * * * * *')

    def test_five_digit_cron_value_init(self):
        cron = Cron('6 20 * * *')
        self.assertTrue(cron.second.value, '00')
        self.assertTrue(cron.minute.value, '6')
        self.assertTrue(cron.hour.value, '6')

    def test_six_digit_cron_value_init(self):
        cron = Cron('20 * * * * *')
        self.assertTrue(cron.second.value, '20')

    def test_cron_time(self):
        self.assertFalse(
            self.cron.is_past_a_datetime(self.datetime_now),
        )


