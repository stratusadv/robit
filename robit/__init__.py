import logging
from robit.worker.worker import Worker
from robit.monitor.monitor import Monitor

FORMAT = 'Process - [%(asctime)-15s] %(message)s'
logging.basicConfig(format=FORMAT)

