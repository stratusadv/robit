import unittest
from http.server import HTTPServer

from robit.web_server.request_handler import WebRequestHandler
from robit.web_server.server import WebServer


class TestServer(unittest.TestCase):
    def setUp(self):
        self.web_server = WebServer()

    def test_start(self):
        pass
        # self.web_server.start()

