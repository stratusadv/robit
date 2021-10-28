import threading
from time import sleep

from .clock import Clock
from .web import WebServer
from .part import Part


class Robit:
    def __init__(self, name, wen_server=True):
        self.name = name
        self.clock = Clock()
        if wen_server:
            self.web_server = WebServer()
        self.part_list = list()

    def add_part(self, name, method):
        self.part_list.append(Part(name, method))

    def run_part_list(self):
        while True:
            for part in self.part_list:
                part.run()

    def run(self):
        thread = threading.Thread(target=self.run_part_list)
        thread.daemon = True
        thread.start()

        while True:
            self.web_server.api_json['parts'] = [part.as_dict() for part in self.part_list]
            sleep(1)

