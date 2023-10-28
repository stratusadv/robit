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
        self.validate_insert(**kwargs)
        db.create_table_if_does_not_exist(self.name, self.fields)
        db.insert(self.name, {'pk': None} | kwargs)

    def validate_insert(self, **kwargs) -> bool:
        for key, val in kwargs.items():
            if key in self.fields:
                if not isinstance(val, TABLE_FIELDS_TYPES[key]):
                    raise ValueError(f'Field "{key}" value of "{val}" is type {type(val)} and should be {TABLE_FIELDS_TYPES[key]}')
            else:
                raise ValueError(f'Field "{key} is not valid for table "{self.name}". Choices are {self.fields.keys()}')

    def select(self, query_conditions: str = '') -> list:
        db = SqliteDB()
        db.cursor.execute(f'SELECT * FROM {self.name} {query_conditions}')

        return db.cursor.fetchall()