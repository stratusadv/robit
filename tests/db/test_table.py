import unittest

from robit.db.table import Table


class TestTable(unittest.TestCase):
    def setUp(self):
        self.table = Table(
            name='unit_test_table',
            fields={
                'tacos': 'INTEGER',
                'type': 'TEXT',
            }
        )

    def test_something(self):
        try:
            self.assertTrue(True)
        except:
            self.assertTrue(False)
