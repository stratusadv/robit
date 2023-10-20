import sqlite3

from robit.config import config


class SqliteDB:
    def __init__(self) -> None:
        self.connection: sqlite3.Connection = ...
        self.cursor: sqlite3.Cursor = ...

    def table_exists(self, table_name: str) -> bool:
        return not self.table_does_not_exists(table_name)

    def table_does_not_exists(self, table_name: str) -> bool:
        self.cursor.execute(f"SELECT name FROM sqlite_master WHERE type='table' AND name='{table_name}'")
        if self.cursor.fetchone() is None:
            return True
        else:
            return False

    def create_table(self, table_name: str, fields: dict) -> None:
        self.open_connection()

        if self.table_does_not_exists(table_name):
            query = f'CREATE TABLE {table_name} ('

            for key, val in fields.items():
                query += f'{key} {val},'

            query += f')'

            self.cursor.execute(query)

        self.commit_and_close_connection()

    def insert(self, table_name: str, fields: dict) -> None:
        self.open_connection()
        if self.table_exists():
            pass

    def open_connection(self):
        self.connection = sqlite3.connect(f'{config.DATABASE_FILE_NAME}_{config.VERSION.replace(".", "_")}.db')
        self.cursor = self.connection.cursor()

    def commit_and_close_connection(self):
        self.connection.commit()
        self.connection.close()
