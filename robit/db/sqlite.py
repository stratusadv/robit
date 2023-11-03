import sqlite3

from robit.config import config


class SqliteDB:
    def __init__(self) -> None:
        self.connection: sqlite3.Connection = ...
        self.cursor: sqlite3.Cursor = ...
        self.open_connection()

    def drop_table(self, table_name):
        self.open_connection()
        self.cursor.execute(f'DROP TABLE IF EXISTS {table_name}')
        self.commit_and_close_connection()

    def table_exists(self, table_name: str) -> bool:
        return not self.table_does_not_exist(table_name)

    def table_does_not_exist(self, table_name: str) -> bool:
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if self.cursor.fetchone() is None:
            return True
        else:
            return False

    def create_table_if_does_not_exist(self, table_name: str, fields: dict) -> None:
        self.open_connection()

        if self.table_does_not_exist(table_name):
            columns_and_types = ', '.join([f'{key} {val}' for key, val in fields.items()])
            query = f'CREATE TABLE {table_name} ({columns_and_types})'

            self.cursor.execute(query)

        self.commit_and_close_connection()

    def insert(self, table_name: str, fields: dict) -> None:
        self.open_connection()

        if self.table_exists(table_name):
            columns = ', '.join(fields.keys())
            placeholders = ', '.join([':' + key for key in fields.keys()])

            query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'

            self.cursor.execute(query, fields)

        self.commit_and_close_connection()

    def open_connection(self):
        self.connection = sqlite3.connect(f'{config.DATABASE_FILE_NAME}_{config.VERSION.replace(".", "_")}.db')
        self.cursor = self.connection.cursor()

    def commit_and_close_connection(self):
        self.connection.commit()
        self.connection.close()
