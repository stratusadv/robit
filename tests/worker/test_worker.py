import unittest

from robit import Worker
from tests.worker.factories import create_test_worker


class TestWorker(unittest.TestCase):
    def setUp(self):
        self.worker = create_test_worker()
        self.worker.add_group('Test Group 1')
        self.worker.add_group('Test Group 2')
        self.worker.add_job('Test Job 1', lambda: None, group='Test Group 1')

    def test_add_group(self):
        self.worker.add_group('Test Group')

        self.assertTrue('Test Group' in self.worker.groups)

    def test_add_job(self):
        self.worker.add_group('Test Group')
        self.worker.add_job('Test Job', lambda: None, group='Test Group')

        self.assertTrue(str(self.worker.groups['Test Group'].job_list[0].name) == 'Test Job')

    def test_calculate_health(self):
        self.worker.calculate_health()

        self.assertTrue(self.worker.health.percentage == 0.5)

