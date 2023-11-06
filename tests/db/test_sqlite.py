import unittest

from robit.db.sqlite import SqliteDB


class TestSqlite(unittest.TestCase):
    def setUp(self):
        self.db = SqliteDB()

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)

