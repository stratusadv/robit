import unittest

from robit.timer.timer import Timer


class TestTimer(unittest.TestCase):
    def setUp(self):
        self.timer = Timer()

    def test_as_dict(self):
        self.assertTrue(self.timer.as_dict()['average_duration'] == '0.00')

    def test_start_stop(self):
        self.timer.start()
        self.timer.longest_duration = -0.01
        self.timer.stop()

        self.assertTrue(self.timer.as_dict()['longest_duration'] == '0.00')

    def test_trim_duration(self):
        self.timer.duration_list_max = 1
        self.timer.start()
        self.timer.stop()
        self.timer.start()
        self.timer.stop()
        self.assertTrue(len(self.timer.duration_list) == 1)
