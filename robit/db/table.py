from robit.db.sqlite import SqliteDB

TABLE_FIELDS_TYPES = {
    'INTEGER': int,
    'INTEGER PRIMARY KEY AUTOINCREMENT': int,
    'TEXT': str,
    'BLOB': str,
    'REAL': float,
}


class Table:
    def __init__(self, name: str, fields: dict[str, str]) -> None:
        self.name = name
        self.fields = {'pk': 'INTEGER PRIMARY KEY AUTOINCREMENT'} | fields

        self.validate_fields()

    def validate_fields(self) -> None:
        for key, val in self.fields.items():
            if val not in TABLE_FIELDS_TYPES:
                raise ValueError(f'Type "{val}" for field "{key}" in table "{self.name}" is not a valid. Choices are {TABLE_FIELDS_TYPES}')

    def insert(self, **kwargs) -> None:
        db = SqliteDB()
        db.create_table_if_does_not_exist(self.name, self.fields)
        # Validate fields and insert ETC
        db.insert(self.name, {
        })

    def validate_insert(self, **kwargs) -> bool:
        for key, val in kwargs.items():
            if key in self.fields:
                if not isinstance(val, TABLE_FIELDS_TYPES[key]):
                    raise ValueError(f'Field "{key}" value of "{val}" is type {type(val)} and should be {TABLE_FIELDS_TYPES[key]}')

        return True

    def select_job_results(job_id: str) -> list:
        db = SqliteDB()
        # Something simple for filtering return results dynamically
        db.cursor.execute(f'SELECT result FROM job_results WHERE job_id="{job_id}"')
        return db.cursor.fetchall()