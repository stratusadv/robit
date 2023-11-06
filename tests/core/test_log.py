import unittest

from robit.core.log import Log


class TestLog(unittest.TestCase):
    def setUp(self):
        self.log = Log()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
