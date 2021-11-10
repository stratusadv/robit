import unittest

from robit import Worker, Monitor


class TestCore(unittest.TestCase):
    def test_worker(self):
        try:
            wo = Worker('Testy McWorkerson')
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_monitor(self):
        try:
            mo = Monitor('Watchy McTesterson')
            self.assertTrue(True)
        except:
            self.assertTrue(False)


