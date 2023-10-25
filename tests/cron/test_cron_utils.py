import unittest

from robit.cron.enums import CronFieldTypeEnum
from robit.cron.utils import CronFieldIdentifier, CronRangeFinder
from robit.cron.fields import CronMinuteField

class TestCronFieldIdentifier(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_every_cron_field(self):
        self.assertEqual(CronFieldIdentifier('*').identify(), CronFieldTypeEnum.EVERY)

    def test_range_cron_field(self):
        self.assertEqual(CronFieldIdentifier('1-10').identify(), CronFieldTypeEnum.RANGE)

    def test_step_cron_field(self):
        self.assertEqual(CronFieldIdentifier('*/5').identify(), CronFieldTypeEnum.STEP)

    def test_list_cron_field(self):
        self.assertEqual(CronFieldIdentifier('1,2,3').identify(), CronFieldTypeEnum.LIST)

    def test_specific_cron_field(self):
        self.assertEqual(CronFieldIdentifier('1').identify(), CronFieldTypeEnum.SPECIFIC)


class TestCronRangeFinder(unittest.TestCase):
    def setUp(self) -> None:
        pass

    def test_every(self):
        minute_field = CronMinuteField('*')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), list(minute_field.value_range))

    def test_list(self):
        minute_field = CronMinuteField('1,2,3')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), [1, 2, 3])

    def test_range(self):
        minute_field = CronMinuteField('1-3')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), [1, 2, 3])

    def test_step(self):
        minute_field = CronMinuteField('*/5')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), [0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55])

    def test_advanced_step(self):
        minute_field = CronMinuteField('0-10/3')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), [0, 3, 6, 9])

    def test_specific(self):
        minute_field = CronMinuteField('1')
        self.assertEqual(CronRangeFinder(minute_field).possible_values(), [1])