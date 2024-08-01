import inspect
import logging
import traceback
from typing import Callable, Optional

from robit.config import config
from robit.core.alert import Alert
from robit.core.clock import Clock, CREATED_DATE_FORMAT
from robit.core.counter import Counter
from robit.cron.cron import Cron
from robit.core.health import Health
from robit.core.id import Id
from robit.core.log import Log
from robit.core.name import Name
from robit.db.utils import datetime_to_string
from robit.job import JobStatus
from robit.job.enums import JobResultType
from robit.job.tables import job_results_table
from robit.timer import Timer, timing_decorator


class Job:
    def __init__(
            self,
            worker: 'Worker',
            group: 'Group',
            name: str,
            method: Callable,
            method_kwargs: Optional[dict] = None,
            cron: str = '* * * * *',
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
            alert_health_threshold: float = 95.0,
            retry_attempts: int = 0
    ) -> None:
        self.worker = worker
        self.group = group
        self.id = Id()
        self.name = Name(name)
        self.method = method

        if method_kwargs is None:
            self.method_kwargs = dict()
        else:
            self.method_kwargs = method_kwargs

            if 'worker' in self.method_kwargs:
                raise ValueError(
                    f'Job method kwargs contains reserved argument "worker". This argument is provided to all jobs for access the worker object.')

        self.cron = Cron(cron_syntax=cron)
        self.next_run_datetime = self.cron.next_datetime()

        if alert_method is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs,
                health_threshold=alert_health_threshold,
            )
        else:
            self.alert = None

        self.clock = Clock()
        self.timer = Timer()
        self.status = JobStatus.QUEUED

        self.success_count = Counter()
        self.failed_count = Counter()
        self.failed_log = Log(max_messages=10)

        self.health = Health()

        self.result_log = Log(max_messages=10)

        self.retry_attempts = retry_attempts

    @timing_decorator
    def execute_method(self):
        if 'worker' in inspect.getfullargspec(self.method).args:
            method_result = self.method(worker=self.worker, **self.method_kwargs)
        else:
            method_result = self.method(**self.method_kwargs)

        return method_result

    @property
    def method_verbose(self) -> str:
        if self.method_kwargs:
            return f'{self.method.__name__}(kwargs={self.method_kwargs})'
        else:
            return f'{self.method.__name__}()'

    def next_run_datetime_verbose(self) -> str:
        return self.next_run_datetime.strftime(CREATED_DATE_FORMAT)

    def set_next_run_datetime(self) -> None:
        self.next_run_datetime = self.cron.next_datetime()

    def should_run(self) -> bool:
        if self.status == JobStatus.QUEUED or self.status == JobStatus.ERROR:
            return self.clock.now_tz > self.next_run_datetime
        else:
            return False

    def run(self) -> None:
        self.status = JobStatus.RUN
        logging.debug(f'STARTING: Job "{self.name}"')

        for attempt in range(self.retry_attempts + 1):
            try:
                self.run_method()
                break
            except Exception as e:
                if attempt >= self.retry_attempts:
                    self.handle_run_exception(e)
                    break
                else:
                    self.status = JobStatus.RETRY
                    logging.warning(f'RETRYING: Job "{self.name}" after failing on exception "{e}" attempt {attempt + 1} of {self.retry_attempts}')
        else:
            logging.error(f'CRITICAL: Job "{self.name}" failed to run and produced no exceptions')

        if self.alert:
            self.alert.check_health_threshold(f'Job "{self.name}"', self.health)

    def run_method(self) -> None:
        method_result = self.execute_method()
        logging.debug(f'SUCCESS: Job "{self.name}" completed')

        self.success_count.increase()

        self.group.success_count.increase()
        self.worker.success_count.increase()

        self.health.add_positive()

        if method_result:
            result_message = str(method_result)
        else:
            result_message = 'No result provided'

        self.result_log.add_message(result_message)
        if config.DATABASE_LOGGING:
            job_results_table.insert(
                job_id=str(self.id),
                job_name=str(self.name),
                type=str(JobResultType.COMPLETED),
                message=result_message,
                datetime_entered=datetime_to_string(self.clock.now_tz)
            )

        self.status = JobStatus.QUEUED

    def handle_run_exception(self, e) -> None:
        self.status = JobStatus.ERROR

        stack_trace = '\n'.join([
            ''.join(traceback.format_exception(None, e, e.__traceback__)).strip()
        ])

        failed_message = f'FAILURE: Job "{self.name}" failed on exception "{e}"\n{stack_trace}'

        logging.error(failed_message)

        if config.DATABASE_LOGGING:
            job_results_table.insert(
                job_id=str(self.id),
                job_name=str(self.name),
                type=str(JobResultType.ERRORED),
                message=failed_message,
                datetime_entered=datetime_to_string(self.clock.now_tz)
            )

        self.failed_log.add_message(failed_message)
        self.failed_count.increase()

        self.group.failed_count.increase()
        self.worker.failed_count.increase()

        self.health.add_negative()

    def as_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': str(self.name),
            'status': str(self.status),
            'next_run_datetime': self.next_run_datetime_verbose(),
            'health': str(self.health),
            'success_count': self.success_count.total,
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
