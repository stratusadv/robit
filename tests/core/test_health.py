import unittest

from robit.core.health import Health


class TestHealth(unittest.TestCase):
    def setUp(self):
        self.health = Health()
        self.health.positive_count = 20
        self.health.negative_count = 5

    def test_string_output(self):
        self.assertTrue(repr(self.health) == '100.00')

    def test_average(self):
        self.health.average(0.5)
        self.assertTrue(self.health.percentage == 0.75)

        self.health.average_reset = True
        self.health.average(0.5)
        self.assertTrue(self.health.percentage == 0.5)

    def test_calculate(self):
        self.health.calculate()
        self.assertTrue(self.health.percentage == 0.80)

    def test_add_negative(self):
        self.health.add_negative(15)
        self.assertTrue(self.health.percentage == 0.50)

        self.health.add_negative(777)
        self.assertTrue(self.health.negative_count == 100)

    def test_add_positive(self):
        self.health.add_positive(25)
        self.assertTrue(self.health.percentage == 0.90)

        self.health.add_positive(555)
        self.assertTrue(self.health.positive_count == 100)

    def test_reset(self):
        self.health.reset()
        self.assertTrue(self.health.percentage == 0.00)
        self.assertTrue(self.health.average_reset == True)

    def test_set_percentage(self):
        self.health.set_percentage(0.5)
        self.assertTrue(self.health.percentage == 0.50)

        self.health.set_percentage(8.2)
        self.assertTrue(self.health.percentage == 1.00)

        self.health.set_percentage(-2.4)
        self.assertTrue(self.health.percentage == 0.00)

    def test_as_dict(self):
        self.assertTrue(self.health.as_dict()['percentage'] == 1.00)
