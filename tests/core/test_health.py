import unittest

from robit.core.health import Health


class TestHealth(unittest.TestCase):
    def setUp(self):
        self.health = Health()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
