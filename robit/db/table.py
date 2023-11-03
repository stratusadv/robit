from robit.db.sqlite import SqliteDB

TABLE_FIELDS_TYPES = {
    'INTEGER': int,
    'INTEGER PRIMARY KEY AUTOINCREMENT': int,
    'TEXT': str,
    'REAL': float,
}


class Table:
    def __init__(self, name: str, fields: dict[str, str], max_rows: int = 1_000_000) -> None:
        self.name = name
        self.fields = {'pk': 'INTEGER PRIMARY KEY AUTOINCREMENT'} | fields
        self.max_rows = max_rows
        self.validate_fields()

    def clean(self):
        db = SqliteDB()
        db.cursor.execute(f'''
            WITH RowCount AS (
                SELECT COUNT(*) as cnt FROM {self.name}
            )
            
            DELETE FROM {self.name}
            WHERE pk NOT IN (
                SELECT pk
                FROM {self.name}
                ORDER BY pk DESC
                LIMIT {self.max_rows * 0.90}
            )
            AND (SELECT cnt FROM RowCount) > {self.max_rows};
        ''')
        db.commit_and_close_connection()

    def drop(self):
        db = SqliteDB()
        db.drop_table(self.name)

    def validate_fields(self) -> None:
        for key, val in self.fields.items():
            if val not in TABLE_FIELDS_TYPES:
                raise ValueError(f'Type "{val}" for field "{key}" in table "{self.name}" is not a valid. Choices are {TABLE_FIELDS_TYPES}')

    def insert(self, **kwargs) -> None:
        db = SqliteDB()
        self.validate_insert(**kwargs)
        db.create_table_if_does_not_exist(self.name, self.fields)
        db.insert(self.name, {'pk': None} | kwargs)
        self.clean()

    def validate_insert(self, **kwargs) -> None:
        for key, val in kwargs.items():
            if key in self.fields:
                if not isinstance(val, TABLE_FIELDS_TYPES[self.fields[key]]):
                    raise ValueError(f'Field "{key}" value of "{val}" is type {type(val)} and should be {TABLE_FIELDS_TYPES[key]}')
            else:
                raise ValueError(f'Field "{key}" is not valid for table "{self.name}". Choices are {self.fields.keys()}')

    def select(self, query_conditions: str = '') -> list:
        db = SqliteDB()
        db.cursor.execute(f'SELECT * FROM {self.name} {query_conditions}')

        return db.cursor.fetchall()

    def select_rows(self, query_conditions: str = '') -> list:
        select_results = self.select(query_conditions)
        rows = []

        for result in select_results:
            row_detail = {}

            for index, key in enumerate(self.fields.keys()):
                row_detail[key] = result[index]

            rows.append(row_detail)

        return rows
