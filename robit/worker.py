from .clock import Clock
from .group import Group
from .health import Health
from .id import Id
from .name import Name
from .status import Status
from .web import WebServer


class Worker:
    def __init__(self, name: str, web_server: bool = True):
        self.id = Id()
        self.name = Name(name)
        self.clock = Clock()
        self.health = Health()
        self.status = Status()

        if web_server:
            self.web_server = WebServer()
        else:
            self.web_server = None

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

    def stop(self):
        pass
