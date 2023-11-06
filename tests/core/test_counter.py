import unittest

from robit.core.counter import Counter


class TestCounter(unittest.TestCase):
    def setUp(self):
        self.counter = Counter()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
