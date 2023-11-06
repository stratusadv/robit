import unittest

from robit import Worker


class TestWorker(unittest.TestCase):
    def test_init(self):
        try:
            wo = Worker('Testy McWorkerson')
            self.assertTrue(True)
        except:
            self.assertTrue(False)
