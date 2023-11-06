import unittest

from robit.core.id import Id


class TestId(unittest.TestCase):
    def setUp(self):
        self.the_id = Id()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
