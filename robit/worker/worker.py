from concurrent.futures import ThreadPoolExecutor
from typing import Callable, Optional
import queue

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.job.group import Group
from robit.core.health import Health
from robit.core.id import Id
from robit.core.name import Name
from robit.core.status import Status
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
        self.status = Status()

        if web_server:
            self.web_server = WorkerWebServer(
                address=web_server_address,
                port=web_server_port,
                key=key,
                html_replace_dict={'title': str(self.name)}
            )

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
            'status': str(self.status),
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
        # Todo: Needs to run it it's own thread
        job = self.queue.get()
        result = job.run()
        print(result)
        print(f'Job "{job.name}" completed')
        self.queue.task_done()

    def start(self) -> None:
        # if self.web_server:
        #     self.web_server.start()

        # Return all jobs that are ready to be executed
        job_list = [self.queue.put(job) for group in self.groups.values() for job in group.job_list]

        for job in job_list:
            self.thread_pool.submit(self.process_queue)

        # Pass the jobs to the queue

        # Separate thread that is processing the queue

        # group_map = {executor.submit(group.start): group for group in self.groups.values()}
        #
        # for future in as_completed(group_map):
        #     print(f'{group_map[future].name} Completed')
        #     # completed_job = job_list[future]
        #     # completed_jobs.append((completed_job, future.result()))
        #
        # # Todo: Need to simplify this
        # # Todo: This needs to be responsive. Do i need to have this ore event based?
        # self.calculate_health()
        #
        # if self.alert:
        #     self.alert.check_health_threshold(f'Worker "{self.name}"', self.health)
        #
        # if self.web_server:
        #     self.web_server.update_api_dict(self.as_dict())
        #
        # if self.monitor_address:
        #     post_worker_data_to_monitor(self.monitor_address, self.monitor_key, self.as_dict_to_monitor())
        #
        # sleep(1)

    def stop(self):
        pass
