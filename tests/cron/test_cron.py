import unittest

from robit.cron.cron import Cron


class TestCron(unittest.TestCase):
    def setUp(self):
        self.cron = Cron('* * * * * *')

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
