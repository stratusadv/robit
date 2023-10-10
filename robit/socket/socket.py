import json
import logging
import socket
from abc import ABC, abstractmethod

DEFAULT_HOST = '127.0.0.1'
DEFAULT_PORT = 8300


class Socket(ABC):
    def __init__(self, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self) -> None:
        self.socket.close()

    @abstractmethod
    def start(self) -> None:
        pass


class ClientSocket(Socket):
    def start(self) -> None:
        self.socket.connect((self.host, self.port))

    def send(self, data: str) -> None:
        self.socket.send(json.dumps(data).encode('utf-8'))


class ServerSocket(Socket):
    @abstractmethod
    def process_requests(self) -> None:
        pass

    def start(self) -> None:
        logging.warning(f'Starting server on {self.host}:{self.port}')
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)
        logging.warning(f'Server started on {self.host}:{self.port}')


class WebServerSocket(ServerSocket):
    def __init__(self, web_server, host: str = DEFAULT_HOST, port: int = DEFAULT_PORT) -> None:
        super().__init__(host, port)
        self.web_server = web_server

    def process_requests(self) -> None:
        while True:
            client, address = self.socket.accept()
            json_string = ''
            while True:
                data = client.recv(1024)

                if data:
                    json_string += data.decode('utf-8')
                else:
                    if json_string:
                        self.web_server.update_api_dict(json.loads(json_string))
                    break

            client.close()
