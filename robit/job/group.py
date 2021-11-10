import threading

from robit.core.clock import Clock
from robit.core.health import Health
from robit.core.id import Id
from robit.job import Job
from robit.core.name import Name
from robit.core.status import Status


class Group:
    def __init__(
            self,
            name: str = 'default',
            utc_offset: int = 0
    ):
        self.id = Id()
        self.name = Name(name)
        self.health = Health()
        self.status = Status()
        self.clock = Clock(utc_offset=utc_offset)

        self.job_list = list()

        self.thread = threading.Thread(target=self.run_job_list)
        self.thread.daemon = True

    def add_job(self, name: str, method, **kwargs):
        self.job_list.append(Job(name=name, method=method, utc_offset=self.clock.utc_offset, **kwargs))

    def calculate_jobs_to_list(self):
        job_list = list()
        self.health.reset()

        for job in self.job_list:
            job_list.append(job.as_dict())
            self.health.average(job.health.percentage)

        return job_list

    def run_job_list(self):
        while True:
            for job in self.job_list:
                job.run()

    def restart(self):
        pass

    def start(self):
        self.thread.start()

    def stop(self):
        pass

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'health': self.health.__str__(),
            'jobs': self.calculate_jobs_to_list(),
            'status': self.status.__str__(),
        }