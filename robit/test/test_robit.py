import unittest
import datetime
import decimal
import json

from robit import Worker, Monitor

wo = Worker('Testy McWorkerson')
mo = Monitor('Watchy McTesterson')


class TestRobit(unittest.TestCase):
    def test_robit(self):
        self.assertTrue(True)

