from time import sleep

from .clock import Clock
from .web import WebServer


class Robit:
    def __init__(self, name):
        self.name = name
        self.clock = Clock()
        self.web_server = WebServer()

    def run(self):
        for i in range(20):
            print(i)
            sleep(1)