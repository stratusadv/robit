class Config:
    TIMEZONE: str = 'UTC'
    LOG_FILE_NAME: str = 'robit.log'
    LOG_BACKUP_DAYS: int = 7
    DATABASE_FILE_NAME: str = 'robit.db'


config = Config()
