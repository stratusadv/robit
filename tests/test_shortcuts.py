import unittest

from robit import shortcuts


class TestShortcuts(unittest.TestCase):
    def test_set_database_file_name(self):
        shortcuts.set_database_file_name('test_name.db')
        self.assertTrue(shortcuts._config.DATABASE_FILE_NAME == 'test_name.db')

    def test_set_log_file_name(self):
        shortcuts.set_log_file_name('test_log')
        self.assertTrue(shortcuts._config.LOG_FILE_NAME == 'test_log')

    def test_set_log_backup_days(self):
        shortcuts.set_log_backup_days(5)
        self.assertTrue(shortcuts._config.LOG_BACKUP_DAYS == 5)

    def test_set_database_logging(self):
        shortcuts.set_database_logging(True)
        self.assertTrue(shortcuts._config.DATABASE_LOGGING is True)

    def test_set_time_zone(self):
        shortcuts.set_timezone('America/Edmonton')
        self.assertTrue(shortcuts._config.TIMEZONE == 'America/Edmonton')
