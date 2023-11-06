import unittest

from robit.db.sqlite import SqliteDB


class TestJob(unittest.TestCase):
    def test_init(self):
        try:
            db = SqliteDB()
            self.assertTrue(True)
        except:
            self.assertTrue(False)

