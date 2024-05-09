import unittest
from datetime import timedelta

from robit.cron.cron import Cron


class TestCron(unittest.TestCase):
    def setUp(self):
        self.cron = Cron('* * * * * *')

    def test_next_datetime(self):
        now = self.cron.clock.now_tz
        next_dt = now.replace(microsecond=0)

        self.assertTrue(self.cron.next_datetime() == next_dt + timedelta(seconds=1))
