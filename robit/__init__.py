import logging
from robit.worker.worker import Worker
from robit.monitor.monitor import Monitor
from robit.config import config


def set_utc_offset(utc_offset: int):
    config.UTC_OFFSET = utc_offset


logging.basicConfig(
    format='Process - - [%(asctime)-15s] %(message)s -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

