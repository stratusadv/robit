import multiprocessing
import queue
import os
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Callable, Optional

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.job.group import Group
from robit.core.health import Health
from robit.core.id import Id
from robit.core.name import Name
from robit.web_server.server import WebServer


class Worker:
    def __init__(
            self,
            name: str,

            web_server: bool = False,
            web_server_address: str = '127.0.0.1',
            web_server_port: int = 8100,

            key: Optional[str] = None,

            max_thread_workers: int = os.cpu_count() * 2,

            alert_method: Optional[Callable] = None,
            alert_method_kwargs: Optional[dict] = None,
    ):
        self.id = Id()
        self.name = Name(name)

        self.queue = queue.Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=max_thread_workers)


        self.clock = Clock()
        self.health = Health()

        self.web_server_conn = None

        if web_server:
            self.web_server = WebServer(
                address=web_server_address,
                port=web_server_port,
                key=key,
                html_replace_dict={'title': str(self.name)}
            )

        if alert_method is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs
            )
        else:
            self.alert = None

        self.groups: dict[str: Group] = dict()

    def add_group(self, name: str, **kwargs) -> None:
        if name not in self.groups:
            self.groups[name] = Group(name=name, **kwargs)

    def add_job(self, name: str, method: Callable, group: str = 'Unnamed Group', **kwargs) -> None:
        self.add_group(group)
        self.groups[group].add_job(name, method, **kwargs)

    def as_dict(self) -> dict:
        return {
            'id': str(self.id),
            'name': str(self.name),
            'groups': [group.as_dict() for group in self.groups.values()],
            'health': str(self.health),
            'clock': self.clock.as_dict(),
            'job_details': self.job_detail_dict()
        }

    def calculate_health(self) -> None:
        self.health.reset()

        for group in self.groups.values():
            group.calculate_health()
            self.health.average(group.health.percentage)

    def job_detail_dict(self) -> dict:
        job_detail_dict = dict()

        for group in self.groups.values():
            job_detail_dict = {**job_detail_dict, **group.job_list_as_dict_full()}

        return job_detail_dict

    def restart(self):
        pass

    def process_queue(self):
        # Pass all the queued jobs to the thread pool
        while not self.queue.empty():
            job = self.queue.get()
            self.thread_pool.submit(job.run)
            self.queue.task_done()

    def add_jobs_to_queue(self):
        ready_jobs = [job for group in self.groups.values() for job in group.job_list if job.should_run()]
        for job in ready_jobs:
            self.queue.put(job)
            job.set_next_run_datetime()
            job.status.waiting()

    def update_web_server(self):
        self.web_server_conn.send(self.as_dict())

    def start(self) -> None:
        if self.web_server:
            self.web_server_conn, self.web_server.worker_conn = multiprocessing.Pipe()
            multiprocessing.Process(target=self.web_server.start).start()

        while True:
            # Continually adds ready jobs to the queue
            self.update_web_server()
            self.add_jobs_to_queue()
            self.process_queue()
            self.calculate_health()
            if self.alert:
                self.alert.check_health_threshold(f'Worker "{self.name}"', self.health)
            sleep(1)

    def stop(self):
        pass
