from time import sleep
from typing import Callable, Optional

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.web_client import post_worker_data_to_monitor
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

        if 'alert_method' is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs
            )

        self.group_dict = dict()

    def add_group(
            self,
            name: str,
            **kwargs
    ):
        if name not in self.group_dict:
            self.group_dict[name] = Group(name=name, **kwargs)

    def add_job(
            self,
            name: str,
            method: Callable,
            group: str = 'Default',
            **kwargs
    ):
        self.add_group(group)
        self.group_dict[group].add_job(name, method, **kwargs)

    def as_dict(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            'groups': self.convert_groups_to_dict_list(),
            'health': str(self.health),
            'status': str(self.status),
            'clock': self.clock.as_dict(),
            'job_details': self.job_detail_dict()
        }

    def as_dict_to_monitor(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            'health': str(self.health),
            'clock': self.clock.as_dict(),
        }

    def calculate_health(self):
        self.health.reset()

        for group in self.group_dict.values():
            self.health.average(group.health.percentage)

    def convert_groups_to_dict_list(self):
        return [group.as_dict() for group in self.group_dict.values()]

    def job_detail_dict(self):
        job_detail_dict = dict()

        for group in self.group_dict.values():
            job_detail_dict = {**job_detail_dict, **group.job_list_as_dict_full()}

        return job_detail_dict

    def restart(self):
        pass

    def run_group_dict(self):
        for group in self.group_dict.values():
            group.start()

    def start(self):
        if self.web_server:
            self.web_server.start()

        self.run_group_dict()

        while True:
            self.calculate_health()

            if self.alert:
                self.alert.check_health_threshold(f'Worker "{self.name}"', self.health)

            if self.web_server:
                self.web_server.update_api_dict(self.as_dict())

            if self.monitor_address:
                post_worker_data_to_monitor(self.monitor_address, self.monitor_key, self.as_dict_to_monitor())
            sleep(1)

    def stop(self):
        pass
