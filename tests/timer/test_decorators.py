import unittest

from robit.timer.decorators import timing_decorator


class TestDecorators(unittest.TestCase):
    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

