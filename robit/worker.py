import threading

from .clock import Clock
from .web import WebServer
from .job import Job


class Worker:
    def __init__(self, name: str, web_server: bool = True):
        self.name = name
        self.clock = Clock()

        if web_server:
            self.web_server = WebServer()

        self.health = 100.0
        self.job_list = list()

    def add_job(self, name, method):
        self.job_list.append(Job(name, method))

    def run_job_list(self):
        while True:
            for job in self.job_list:
                job.run()

    def run(self):
        thread = threading.Thread(target=self.run_job_list)
        thread.daemon = True
        thread.start()

        while True:
            self.web_server.api_json['jobs'] = [job.as_dict() for job in self.job_list]
            self.web_server.api_json['health'] = self.health

