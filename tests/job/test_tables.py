from datetime import datetime
import unittest

from robit.job.tables import job_results_table
from robit.db.utils import datetime_to_string


class TestTables(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        job_results_table.drop()

    def test_job_result_insert(self):
        try:
            job_results_table.insert(
                job_id='abc123',
                job_name='A Job of Sorts',
                type='something',
                message='A bunch of text that resembles a result',
                datetime_entered=datetime_to_string(datetime.now())
            )
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_job_result_select(self):
        rows = job_results_table.select(query_conditions=f'WHERE job_id="abc123"')
        self.assertTrue(len(rows) > 0)


