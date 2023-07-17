import unittest
from datetime import datetime
from robit.core import cron_wes as cron


class TestCronIdentifier(unittest.TestCase):
    def test_every_value(self):
        cron_field = cron.CronMinuteField('*')
        cron_identifier = cron.CronIdentifier(cron_field)
        self.assertEqual(cron_identifier.identify(), 'every')

    def test_range_value(self):
        cron_field = cron.CronMinuteField('1-5')
        cron_identifier = cron.CronIdentifier(cron_field)
        self.assertEqual(cron_identifier.identify(), 'range')

    def test_step_value(self):
        cron_field = cron.CronMinuteField('*/5')
        cron_identifier = cron.CronIdentifier(cron_field)
        self.assertEqual(cron_identifier.identify(), 'step')

    def test_list_value(self):
        cron_field = cron.CronMinuteField('1,2,3')
        cron_identifier = cron.CronIdentifier(cron_field)
        self.assertEqual(cron_identifier.identify(), 'list')

    def test_specific_value(self):
        cron_field = cron.CronMinuteField('1')
        cron_identifier = cron.CronIdentifier(cron_field)
        self.assertEqual(cron_identifier.identify(), 'specific')


class TestCronRangeFinder(unittest.TestCase):
    def test_list_value(self):
        cron_field = cron.CronMinuteField('1,2,3')
        range_finder = cron.CronRangeFinder(cron_field)
        self.assertEqual(range_finder.value_range(), [1, 2, 3])

    def test_range_value(self):
        cron_field = cron.CronMinuteField('1-5')
        range_finder = cron.CronRangeFinder(cron_field)
        self.assertEqual(range_finder.value_range(), [1, 2, 3, 4, 5])

    def test_step_value(self):
        cron_field = cron.CronMinuteField('*/5')
        range_finder = cron.CronRangeFinder(cron_field)
        self.assertEqual(range_finder.value_range(), [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

    def test_every_value(self):
        cron_field = cron.CronMinuteField('*')
        range_finder = cron.CronRangeFinder(cron_field)
        self.assertEqual(range_finder.value_range(), list(range(0, 60)))

    def test_specific_value(self):
        cron_field = cron.CronMinuteField('1')
        range_finder = cron.CronRangeFinder(cron_field)
        self.assertEqual(range_finder.value_range(), [1])

    def test_invalid_range_max_value(self):
        with self.assertRaises(ValueError):
            cron.CronMinuteField('1-100')

    def test_invalid_range_min_value(self):
        with self.assertRaises(ValueError):
            cron.CronMinuteField('-1-5')

    def test_invalid_every_value(self):
        with self.assertRaises(ValueError):
            cron.CronMinuteField('invalid')

    def test_invalid_specific_max_value(self):
        with self.assertRaises(ValueError):
            cron.CronMinuteField('90')

    def test_invalid_specific_min_value(self):
        with self.assertRaises(ValueError):
            cron_field = cron.CronMinuteField('-1')

    def test_invalid_list_value(self):
        with self.assertRaises(ValueError):
            cron.CronMinuteField('1,2,3,99')
