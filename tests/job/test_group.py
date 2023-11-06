import unittest

from robit.worker.worker import Worker
from robit.job.group import Group


class TestGroup(unittest.TestCase):
    def setUp(self):
        self.worker = Worker(
            name='Worker McWorkerson'
        )
        self.group = Group(self.worker)

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

