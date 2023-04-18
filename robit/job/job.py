import logging
from time import sleep
from typing import Callable

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.counter import Counter
from robit.core.cron import Cron
from robit.core.health import Health
from robit.core.id import Id
from robit.core.log import Log
from robit.core.name import Name
from robit.core.status import Status
from robit.core.timer import Timer


class Job:
    def __init__(
            self,
            name: str,
            method,
            method_kwargs: dict = {},
            utc_offset: int = 0,
            cron: str = '* * * * * *',
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
    ):
        self.id = Id()
        self.name = Name(name)
        self.method = method
        self.method_kwargs = method_kwargs

        self.cron = Cron(cron_syntax=cron, utc_offset=utc_offset)

        if 'alert_method' is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs
            )
        else:
            self.alert = None

        self.clock = Clock(utc_offset=utc_offset)

        self.timer = Timer()

        self.status = Status()

        self.success_count = Counter()
        self.failed_count = Counter()
        self.failed_log = Log(max_messages=20, utc_offset=utc_offset)

        self.health = Health()

        self.result_log = Log(max_messages=200, utc_offset=utc_offset)

    @property
    def method_verbose(self):
        if self.method_kwargs:
            return f'{self.method.__name__}(kwargs={self.method_kwargs})'
        else:
            return f'{ self.method.__name__ }()'

    def run(self):
        if self.cron.is_past_next_run_datetime():
            self.cron.set_next_run_time()

            logging.warning(f'STARTING: Job "{self.name}"')

            self.status.set('run')
            self.timer.start()

            try:
                if self.method_kwargs:
                    method_result = self.method(**self.method_kwargs)
                else:
                    method_result = self.method()
                self.timer.stop()
                logging.warning(f'SUCCESS: Job "{self.name}" completed')
                self.success_count.increase()
                self.health.add_positive()
                if method_result:
                    self.result_log.add_message(str(method_result))
            except Exception as e:
                self.status.set('error')
                failed_message = f'ERROR: Job "{self.name}" failed on exception "{e}"'
                logging.warning(failed_message)
                self.failed_log.add_message(failed_message)
                self.failed_count.increase()
                self.health.add_negative()

            if self.alert:
                self.alert.check_health_threshold(f'Job "{self.name}"', self.health)
        else:
            if self.status.value != 'error':
                self.status.set('queued')

            sleep(1)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'status': self.status.__str__(),
            'next_run_datetime': self.cron.next_run_datetime_verbose,
            'success_count': self.success_count.total,
            'health': self.health.__str__(),
            'failed_count': self.failed_count.total,
        }

    def as_dict_full(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'method': self.method_verbose,
            'status': self.status.__str__(),
            'result_log': self.result_log.message_list,
            'clock': self.clock.as_dict(),
            'timer': self.timer.as_dict(),
            'success_count': self.success_count.total,
            'health': self.health.__str__(),
            'failed_count': self.failed_count.total,
            'failed_log': self.failed_log.message_list,
        }
