import multiprocessing
from concurrent.futures import ThreadPoolExecutor
from time import sleep
from typing import Callable, Optional
import queue

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.utils import tz_now
from robit.web_server.utils import post_worker_data_to_monitor
from robit.job.group import Group
from robit.core.health import Health
from robit.core.id import Id
from robit.core.name import Name
from robit.socket.socket import ClientSocket
from robit.worker.web_server import WorkerWebServer


class Worker:
    def __init__(
            self,
            name: str,
            web_server: bool = False,
            web_server_address: str = '127.0.0.1',
            web_server_port: int = 8100,
            key: Optional[str] = None,
            monitor_address: Optional[str] = None,
            monitor_port: int = 8200,
            monitor_key: Optional[str] = None,
            alert_method: Optional[Callable] = None,
            alert_method_kwargs: Optional[dict] = None,
    ):
        self.id = Id()
        self.name = Name(name)

        self.queue = queue.Queue()
        self.thread_pool = ThreadPoolExecutor(max_workers=2)

        self.clock = Clock()
        self.health = Health()

        if web_server:
            self.web_server = WorkerWebServer(
                address=web_server_address,
                port=web_server_port,
                key=key,
                html_replace_dict={'title': str(self.name)}
            )
            self.client = None

        self.monitor_address = monitor_address
        self.monitor_port = monitor_port
        self.monitor_key = monitor_key

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

    def as_dict_to_monitor(self) -> dict:
        return {
            'id': str(self.id),
            'name': str(self.name),
            'health': str(self.health),
            'clock': self.clock.as_dict(),
        }

    def calculate_health(self) -> None:
        self.health.reset()

        for group in self.groups.values():
            self.health.average(group.health.percentage)

    def job_detail_dict(self) -> dict:
        job_detail_dict = dict()

        for group in self.groups.values():
            job_detail_dict = {**job_detail_dict, **group.job_list_as_dict_full()}

        return job_detail_dict

    def restart(self):
        pass

    def process_queue(self):
        if not self.queue.empty():
            job = self.queue.get()
            job.run()

            if self.web_server:
                self.update_web_server()

            # Complete job
            self.queue.task_done()

    def add_jobs_to_queue(self):
        ready_jobs = [job for group in self.groups.values() for job in group.job_list if tz_now() > job.next_run_datetime]
        for job in ready_jobs:
            self.queue.put(job)
            job.status.waiting()
            self.thread_pool.submit(self.process_queue)

    def update_web_server(self):
        client_socket = ClientSocket('localhost', 8000)
        client_socket.start()
        client_socket.send(self.as_dict())
        client_socket.close()

        # Todo: Need to update the monitor
        # if self.monitor_address:
        #     post_worker_data_to_monitor(self.monitor_address, self.monitor_key, self.as_dict_to_monitor())

    def start(self) -> None:
        if self.web_server:
            # Start the webserver in a different process and send initial data
            multiprocessing.Process(target=self.web_server.start).start()
            self.update_web_server()

        while True:
            # Continually adds ready jobs to the queue
            self.add_jobs_to_queue()
            self.process_queue()
            self.calculate_health()
            if self.alert:
                self.alert.check_health_threshold(f'Worker "{self.name}"', self.health)
            sleep(1)

    def stop(self):
        pass
