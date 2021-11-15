from time import sleep

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
            utc_offset: int = 0
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

        self.group_dict = dict()

    def add_job(self, name, method, group='Default', **kwargs):
        if group not in self.group_dict:
            self.group_dict[group] = Group(name=group, utc_offset=self.clock.utc_offset)

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
        self.health.reset()

        for group in self.group_dict.values():
            group_list.append(group.as_dict())
            self.health.average(group.health.percentage)

        return group_list

    def job_detail_dict(self):
        job_detail_dict = dict()

        for group in self.group_dict.values():
            job_detail_dict = {**job_detail_dict, **group.job_list_as_dict_full()}

        return job_detail_dict

    def restart(self):
        pass

    def start_all_groups(self):
        for group in self.group_dict.values():
            group.start()

    def start(self):
        if self.web_server:
            self.web_server.start()

        self.start_all_groups()

        while True:
            if self.web_server:
                self.web_server.update_api_dict(self.as_dict())
            if self.monitor_address:
                post_worker_data_to_monitor(self.monitor_address, self.monitor_key, self.as_dict_to_monitor())
            sleep(1)

    def stop(self):
        pass
