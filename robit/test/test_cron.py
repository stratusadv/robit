import unittest
from datetime import datetime

from robit.core.cron import Cron


class TestCron(unittest.TestCase):
    def setUp(self) -> None:
        self.cron = Cron('10 10 1 * * *')
        self.datetime_now = datetime.utcnow().replace(microsecond=0)

    def test_cron_time(self):
        self.assertFalse(
            self.cron.is_past_a_datetime(self.datetime_now),
        )
