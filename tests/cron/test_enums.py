import unittest

from robit.cron import enums


class TestEnums(unittest.TestCase):
    def setUp(self):
        self.enums = enums.CronFieldTypeEnum.STEP

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
