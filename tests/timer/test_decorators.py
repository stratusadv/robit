import unittest

from robit.timer import Timer
from robit.timer.decorators import timing_decorator


class TestDecorators(unittest.TestCase):
    def test_timing_decorator(self):
        try:
            class TestClass:
                def __init__(self):
                    self.timer = Timer()

                @timing_decorator
                def test_func(self):
                    pass

            TestClass().test_func()

            @timing_decorator
            def test_func(self=None):
                pass

            test_func('hi')

            self.assertTrue(True)
        except:
            self.assertTrue(False)
