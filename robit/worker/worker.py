from time import sleep

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
            web_server: bool = True,
            web_server_address: str = '127.0.0.1',
            web_server_port: int = 8000,
            key: str = None,
            monitor_address: str = None,
            monitor_port: int = 8200,
            monitor_key: str = None,
            utc_offset: int = 0,
            **kwargs,
    ):
        self.id = Id()
        self.name = Name(name)
        self.clock = Clock(utc_offset=utc_offset)
        self.health = Health()
        self.status = Status()

        if web_server:
            self.web_server = WorkerWebServer(
                address=web_server_address,
                port=web_server_port,
                key=key,
                html_replace_dict={'title': self.name.__str__()}
            )
        else:
            self.web_server = None

        self.monitor_address = monitor_address
        self.monitor_port = monitor_port
        self.monitor_key = monitor_key

        if 'alert_method' in kwargs:
            self.alert = Alert(**kwargs)
        else:
            self.alert = None

        self.group_dict = dict()

    def add_group(self, name, **kwargs):
        if name not in self.group_dict:
            self.group_dict[name] = Group(name=name, utc_offset=self.clock.utc_offset, **kwargs)

    def add_job(self, name, method, group='Default', **kwargs):
        self.add_group(group)
        self.group_dict[group].add_job(name, method, **kwargs)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'groups': self.calculate_groups_to_list(),
            'health': self.health.__str__(),
            'status': self.status.__str__(),
            'clock': self.clock.as_dict(),
            'job_details': self.job_detail_dict()
        }

    def as_dict_to_monitor(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'health': self.health.__str__(),
            'clock': self.clock.as_dict(),
        }

    def calculate_groups_to_list(self):
        group_list = list()

        for group in self.group_dict.values():
            group_list.append(group.as_dict())

        return group_list

    def calculate_health(self):
        self.health.reset()

        for group in self.group_dict.values():
            self.health.average(group.health.percentage)

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
