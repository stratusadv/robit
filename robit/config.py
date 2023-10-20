class Config:
    VERSION: str = '0.4.4'
    TIMEZONE: str = 'UTC'
    LOG_FILE_NAME: str = 'robit'
    LOG_BACKUP_DAYS: int = 7
    DATABASE_FILE_NAME: str = 'robit'


config = Config()
