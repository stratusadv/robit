import threading
import uuid

from .clock import Clock
from .id import Id
from .web import WebServer
from .job import Job


class Worker:
    def __init__(self, name: str, web_server: bool = True):
        self.id = Id()

        self.name = name
        self.clock = Clock()

        if web_server:
            self.web_server = WebServer()
            self.web_server.run()

        self.job_list = list()

        self.job_list_thread = threading.Thread(target=self.run_job_list)
        self.job_list_thread.daemon = True

    def add_job(self, name, method):
        self.job_list.append(Job(name, method))

    def run_job_list(self):
        while True:
            for job in self.job_list:
                job.run()

    def run(self):
        self.job_list_thread.start()

        while True:
            jobs = list()
            average_health_percentage = 1.0
            for job in self.job_list:
                jobs.append(job.as_dict())
                average_health_percentage = (average_health_percentage + job.health.percentage) / 2

            self.web_server.api_json['id'] = self.id.value
            self.web_server.api_json['name'] = self.name
            self.web_server.api_json['job_list'] = jobs
            self.web_server.api_json['average_job_health'] = average_health_percentage

