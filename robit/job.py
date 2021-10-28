import logging

from robit.counter import Counter
from robit.log import Log
from robit.timer import Timer


class Job:
    def __init__(self, name: str, method):
        self.name = name
        self.method = method
        self.status = False
        self.success_count = Counter()
        self.failed_count = Counter()
        self.failed_log = Log()

    def run(self):
        logging.warning(f'Starting: Job "{self.name}"')
        try:
            self.method()
            logging.warning(f'Success: Job "{self.name}" ran correctly')
            self.success_count.increase()
            self.status = True
        except Exception as e:
            failed_message = f'Failed: Job "{self.name}" on Exception: {e}'
            logging.warning(failed_message)
            self.failed_log.add_message(failed_message)
            self.failed_count.increase()
            self.status = False

    def as_dict(self):
        return {
            'name': self.name,
            'method': self.method.__name__,
            'status': self.status,
            'success_count': self.success_count.total,
            'failed_count': self.failed_count.total,
            'failed_log': self.failed_log.message_list,
        }