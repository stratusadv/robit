import unittest

from robit.core.name import Name


class TestName(unittest.TestCase):
    def setUp(self):
        self.name = Name('Testing Mc Testerson')

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
