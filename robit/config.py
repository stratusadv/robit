from robit.version import VERSION


class Config:
    VERSION: str = VERSION
    TIMEZONE: str = 'UTC'
    LOG_FILE_NAME: str = 'robit'
    LOG_BACKUP_DAYS: int = 7
    DATABASE_LOGGING: bool = False
    DATABASE_FILE_NAME: str = 'robit'
    DATABASE_BACKUP_DAYS: int = 21


config = Config()
