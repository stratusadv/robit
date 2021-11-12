import logging
from time import sleep

from robit.core.clock import Clock
from robit.core.counter import Counter
from robit.core.health import Health
from robit.core.id import Id
from robit.core.log import Log
from robit.core.status import Status


class Job:
    def __init__(
            self,
            name: str,
            method,
            utc_offset: int = 0,
            **kwargs
    ):
        self.id = Id()

        self.name = name

        self.method = method

        if 'method_kwargs' in kwargs:
            self.method_kwargs = kwargs['method_kwargs']
        else:
            self.method_kwargs = None

        if 'cron' in kwargs:
            self.clock = Clock(cron=kwargs['cron'], utc_offset=utc_offset)
        else:
            self.clock = Clock(utc_offset=utc_offset)

        self.status = Status()

        self.success_count = Counter()
        self.failed_count = Counter()
        self.failed_log = Log(max_messages=20)

        self.health = Health()

        self.result_log = Log(max_messages=200)

    @property
    def method_verbose(self):
        if self.method_kwargs:
            return f'{self.method.__name__}(kwargs={self.method_kwargs})'
        else:
            return f'{ self.method.__name__ }()'

    def run(self):
        if self.clock.is_past_next_run_datetime():
            logging.warning(f'Starting: Job "{self.name}"')
            self.status.set('run')
            self.clock.start_timer()
            try:
                if self.method_kwargs:
                    method_result = self.method(**self.method_kwargs)
                else:
                    method_result = self.method()
                self.clock.stop_timer()
                logging.warning(f'Success: Job "{self.name}" ran correctly')
                self.success_count.increase()
                self.health.add_positive()
                if method_result:
                    self.result_log.add_message(str(method_result))
            except Exception as e:
                self.status.set('error')
                failed_message = f'Failed on Exception: {e}'
                logging.warning(failed_message)
                self.failed_log.add_message(failed_message)
                self.failed_count.increase()
                self.health.add_negative()
        else:
            if self.status.value != 'error':
                self.status.set('queued')
            sleep(1)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'status': self.status.__str__(),
            'next_run_datetime': self.clock.next_run_datetime_verbose,
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
            'success_count': self.success_count.total,
            'health': self.health.__str__(),
            'failed_count': self.failed_count.total,
            'failed_log': self.failed_log.message_list,
        }
