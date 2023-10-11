import logging
from robit.worker.worker import Worker
from robit.config import config as _config


def set_utc_offset(utc_offset: int) -> None:
    _config.UTC_OFFSET = utc_offset


logging.basicConfig(
    format='Process - - [%(asctime)-15s] %(message)s -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

