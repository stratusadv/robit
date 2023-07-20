from typing import Callable

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.health import Health
from robit.core.id import Id
from robit.job import Job
from robit.core.name import Name


class Group:
    def __init__(
            self,
            name: str = 'Unnamed Group',
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
            alert_health_threshold: float = 95.0,
    ):
        self.id: Id = Id()
        self.name: Name = Name(name)
        self.health: Health = Health()
        self.clock: Clock = Clock()

        self.job_list: list[Job] = list()

        if alert_method is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs,
                health_threshold=alert_health_threshold
            )
        else:
            self.alert = None

    def add_job(self, name: str, method: Callable, **kwargs):
        self.job_list.append(Job(name=name, method=method, **kwargs))

    def calculate_health(self):
        self.health.reset()

        for job in self.job_list:
            self.health.average(job.health.percentage)

    def convert_jobs_to_dict_list(self):
        return [job.as_dict() for job in self.job_list]

    def job_list_as_dict_full(self):
        job_dict_full = dict()

        for job in self.job_list:
            job_dict_full[str(job.id)] = job.as_dict_full()

        return job_dict_full

    def run_job_list(self):
        while True:
            for job in self.job_list:
                job.run()

            self.calculate_health()

            if self.alert:
                self.alert.check_health_threshold(f'Group "{self.name}"', self.health)

    def restart(self):
        pass

    def start(self):
        pass

    def stop(self):
        pass

    def as_dict(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            'health': str(self.health),
            'jobs': self.convert_jobs_to_dict_list(),
        }
