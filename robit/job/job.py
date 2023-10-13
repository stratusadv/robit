import logging
from typing import Callable, Optional

from robit.core.alert import Alert
from robit.core.clock import Clock, CREATED_DATE_FORMAT
from robit.core.counter import Counter
from robit.cron.cron import Cron
from robit.core.health import Health
from robit.core.id import Id
from robit.core.log import Log
from robit.core.name import Name
from robit.status import Status
from robit.timer import Timer, timing_decorator


class Job:
    def __init__(
            self,
            name: str,
            method: Callable,
            method_kwargs: Optional[dict] = None,
            cron: str = '* * * * *',
            execution_type: str = 'thread',
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
    ) -> None:
        self.id = Id()
        self.name = Name(name)
        self.method = method
        self.execution_type = execution_type

        if method_kwargs is None:
            self.method_kwargs = dict()
        else:
            self.method_kwargs = method_kwargs

        self.cron = Cron(cron_syntax=cron)
        self.next_run_datetime = self.cron.next_datetime()

        if alert_method is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs
            )
        else:
            self.alert = None

        self.clock = Clock()
        self.timer = Timer()
        self.status = Status()

        self.success_count = Counter()
        self.failed_count = Counter()
        self.failed_log = Log(max_messages=10)

        self.health = Health()

        self.result_log = Log(max_messages=10)

    @timing_decorator
    def execute_method(self):
        if self.method_kwargs:
            method_result = self.method(**self.method_kwargs)
        else:
            method_result = self.method()
        return method_result

    @property
    def method_verbose(self) -> str:
        if self.method_kwargs:
            return f'{self.method.__name__}(kwargs={self.method_kwargs})'
        else:
            return f'{ self.method.__name__ }()'

    def next_run_datetime_verbose(self) -> str:
        return self.next_run_datetime.strftime(CREATED_DATE_FORMAT)

    def set_next_run_datetime(self) -> None:
        self.next_run_datetime = self.cron.next_datetime()

    def should_run(self) -> bool:
        return self.clock.now_tz > self.next_run_datetime

    def run(self) -> None:
        self.status.running()

        logging.warning(f'STARTING: Job "{self.name}"')

        try:
            method_result = self.execute_method()
            logging.warning(f'SUCCESS: Job "{self.name}" completed')

            self.success_count.increase()
            self.health.add_positive()

            if method_result:
                self.result_log.add_message(str(method_result))

            self.status.queued()
        except Exception as e:
            self.status.error()
            failed_message = f'ERROR: Job "{self.name}" failed on exception "{e}"'
            logging.warning(failed_message)
            self.failed_log.add_message(failed_message)
            self.failed_count.increase()
            self.health.add_negative()

        if self.alert:
            self.alert.check_health_threshold(f'Job "{self.name}"', self.health)

    def as_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': str(self.name),
            'status': str(self.status),
            'next_run_datetime': self.next_run_datetime_verbose(),
            'success_count': self.success_count.total,
            'health': str(self.health),
            'failed_count': self.failed_count.total,
        }

    def as_dict_full(self) -> dict:
        return self.as_dict() | {
            'method': self.method_verbose,
            'result_log': list(self.result_log.messages),
            'clock': self.clock.as_dict(),
            'timer': self.timer.as_dict(),
            'failed_log': list(self.failed_log.messages),
        }
