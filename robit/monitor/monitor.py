from time import sleep
from typing import Callable

from robit.core.alert import Alert
from robit.core.clock import Clock
from robit.core.health import Health
from robit.core.id import Id
from robit.core.name import Name
from robit.monitor.web_server import MonitorWebServer


class Monitor:
    def __init__(
            self,
            name: str,
            web_server: bool = True,
            web_server_address: str = '127.0.0.1',
            web_server_port: int = 8200,
            key: str = None,
            alert_method: Callable = None,
            alert_method_kwargs: dict = None,
    ):
        self.id = Id()
        self.name = Name(name)
        self.clock = Clock()
        self.health = Health()

        if web_server:
            self.web_server = MonitorWebServer(
                address=web_server_address,
                port=web_server_port,
                key=key,
                html_replace_dict={'title': str(self.name)}
            )
            self.web_server.post_dict['worker_dict'] = dict()
        else:
            self.web_server = None

        if 'alert_method' is not None:
            self.alert = Alert(
                method=alert_method,
                method_kwargs=alert_method_kwargs
            )
        else:
            self.alert = None

        self.worker_dict = self.web_server.post_dict['worker_dict']

    def as_dict(self):
        return {
            'id': str(self.id),
            'name': str(self.name),
            'health': str(self.health),
            'clock': self.clock.as_dict(),
            'workers': self.calculate_workers_to_list(),
        }

    def calculate_health(self):
        self.health.reset()

        for worker in self.worker_dict.values():
            self.health.average(float(worker['health']) * 0.01)

    def calculate_workers_to_list(self):
        worker_list = list()

        for worker in self.worker_dict.values():
            worker_list.append(worker)

        return worker_list

    def restart(self):
        pass

    def start(self):
        if self.web_server:
            self.web_server.start()

        while True:
            self.calculate_health()

            if self.alert:
                self.alert.check_health_threshold(f'Monitor "{self.name}"', self.health)

            if self.web_server:
                self.web_server.update_api_dict(self.as_dict())

            sleep(1)

    def stop(self):
        pass
