from time import sleep

from robit.core.clock import Clock
from robit.core.health import Health
from robit.core.id import Id
from robit.core.name import Name
from robit.core.status import Status
from robit.monitor.web_server import MonitorWebServer


class Monitor:
    def __init__(self, name: str, web_server: bool = True, web_server_port: int = 8200, key: str = None):
        self.id = Id()
        self.name = Name(name)
        self.clock = Clock()
        self.health = Health()
        self.status = Status()

        if web_server:
            self.web_server = MonitorWebServer(port=web_server_port, key=key)
            self.web_server.post_dict['worker_dict'] = dict()
        else:
            self.web_server = None

        self.worker_dict = self.web_server.post_dict['worker_dict']
        # self.monitor_dict = dict()

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'health': self.health.__str__(),
            'status': self.status.__str__(),
            'created': self.clock.created_tz_verbose,
            'workers': self.calculate_workers_to_list(),
        }

    def calculate_workers_to_list(self):
        worker_list = list()
        self.health.reset()

        for worker in self.worker_dict.values():
            # print(worker)
            worker_list.append(worker)
            self.health.average(float(worker['health']) * 0.01)

        return worker_list

    def restart(self):
        pass

    def start(self):
        if self.web_server:
            self.web_server.start()

        while True:
            if self.web_server:
                self.web_server.update_api_dict(self.as_dict())
                # print(self.worker_dict)
                sleep(1)


    def stop(self):
        pass