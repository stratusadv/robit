from typing import Callable

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.counter import Counter
from robit.core.health import Health
from robit.core.id import Id
from robit.job import Job
from robit.core.name import Name


class Group:
    def __init__(
            self,
            worker: 'Worker',
            name: str = 'Unnamed Group',
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
            alert_health_threshold: float = 95.0,
    ) -> None:
        self.worker = worker
        self.id: Id = Id()
        self.name: Name = Name(name)
        self.health: Health = Health()
        self.clock: Clock = Clock()

        self.success_count = Counter()
        self.failed_count = Counter()

        self.job_list: list[Job] = list()

        if alert_method is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs,
                health_threshold=alert_health_threshold,
            )
        else:
            self.alert = None

    def add_job(self, name: str, method: Callable, **kwargs) -> None:
        self.job_list.append(Job(worker=self.worker, group=self, name=name, method=method, **kwargs))

    def calculate_health(self) -> None:
        self.health.reset()

        for job in self.job_list:
            self.health.average(job.health.percentage)

    def job_list_as_dict_full(self) -> dict:
        job_dict_full = dict()

        for job in self.job_list:
            job_dict_full[str(job.id)] = job.as_dict_full()

        return job_dict_full

    def as_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': str(self.name),
            'health': str(self.health),
            'jobs': [job.as_dict() for job in self.job_list],
            'success_count': self.success_count.total,
            'failed_count': self.failed_count.total,
        }