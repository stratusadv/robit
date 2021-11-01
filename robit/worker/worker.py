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
    def __init__(self, name: str, web_server: bool = True, web_server_port: int = 8000, key: str = None, monitor_address: str = None, monitor_key: str = None):
        self.id = Id()
        self.name = Name(name)
        self.clock = Clock()
        self.health = Health()
        self.status = Status()

        if web_server:
            self.web_server = WorkerWebServer(port=web_server_port, key=key)
        else:
            self.web_server = None

        self.monitor_address = monitor_address
        self.monitor_key = monitor_key

        self.group_dict = dict()

    def add_job(self, name, method, group='Default'):
        if group not in self.group_dict:
            self.group_dict[group] = Group(name=group)

        self.group_dict[group].add_job(name, method)

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'groups': self.calculate_groups_to_list(),
            'health': self.health.__str__(),
            'status': self.status.__str__(),
            'created': self.clock.created_tz_verbose
        }

    def as_dict_to_monitor(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'health': self.health.__str__(),
            'created': self.clock.created_tz_verbose
        }

    def calculate_groups_to_list(self):
        group_list = list()
        self.health.reset()

        for group in self.group_dict.values():
            group_list.append(group.as_dict())
            self.health.average(group.health.percentage)

        return group_list

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
