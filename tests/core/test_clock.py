import unittest
from datetime import datetime, timedelta
from robit.core.clock import Clock, CREATED_DATE_FORMAT


class TestClock(unittest.TestCase):

    def test_init(self):
        try:
            clock = Clock()
            self.assertTrue(True)
        except:
            self.assertTrue(False)
