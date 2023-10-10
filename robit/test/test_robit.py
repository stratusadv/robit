import unittest

from robit import Worker


class TestCore(unittest.TestCase):
    def test_worker(self):
        try:
            wo = Worker('Testy McWorkerson')
            self.assertTrue(True)
        except:
            self.assertTrue(False)
