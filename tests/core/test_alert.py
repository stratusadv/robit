import unittest

from robit.core.alert import Alert


class TestAlert(unittest.TestCase):
    def setUp(self):
        def hello_world():
            print('Hello World from Alert')

        self.alert = Alert(hello_world)

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
