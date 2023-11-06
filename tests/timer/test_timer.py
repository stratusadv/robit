import unittest

from robit.timer.timer import Timer


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

