import logging
from logging.handlers import TimedRotatingFileHandler

from robit.worker.worker import Worker
from robit.config import config as _config
from robit.shortcuts import *


timed_rotating_log_handler = TimedRotatingFileHandler(
    f'{_config.LOG_FILE_NAME}.log',
    delay=True,
    when='midnight',
    backupCount=_config.LOG_BACKUP_DAYS,
)
timed_rotating_log_handler.setLevel(logging.WARNING)

stream_log_handler = logging.StreamHandler()
stream_log_handler.setLevel(logging.DEBUG)

logging.basicConfig(
    level=logging.DEBUG,
    format='Process - %(levelname)s - [%(asctime)-15s] %(message)s',
    datefmt='%d/%b/%Y %H:%M:%S',
    handlers=[
        timed_rotating_log_handler,
        stream_log_handler,
    ]
)

