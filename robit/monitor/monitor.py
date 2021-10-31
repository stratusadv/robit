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
        else:
            self.web_server = None

    def as_dict(self):
        return {
            'id': self.id.__str__(),
            'name': self.name.__str__(),
            'health': self.health.__str__(),
            'status': self.status.__str__(),
            'created': self.clock.created_tz_verbose
        }

    def restart(self):
        pass

    def start(self):
        if self.web_server:
            self.web_server.start()

        while True:
            if self.web_server:
                self.web_server.update_api_dict(self.as_dict())

    def stop(self):
        pass