import logging
from robit.worker.worker import Worker
from robit.monitor.monitor import Monitor

logging.basicConfig(
    format='Process - - [%(asctime)-15s] %(message)s -',
    datefmt='%d/%b/%Y %H:%M:%S'
)

