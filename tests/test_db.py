import unittest


class TestDatabase(unittest.TestCase):
    def test_insert(self):
        try:
            from robit.db.utils import insert_job_result

            insert_job_result(
                '12345',
                'Some Type of Job',
                'A result of the best kind',
            )
            self.assertTrue(True)
        except:
            self.assertTrue(False)

    def test_select(self):
        from robit.db.utils import select_job_results
        results = select_job_results('12345')
        if len(results) > 0:
            self.assertTrue(True)
        else:
            self.assertTrue(False)