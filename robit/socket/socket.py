import json
import socket
from abc import ABC, abstractmethod


class Socket(ABC):
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def close(self):
        self.socket.close()

    @abstractmethod
    def start(self):
        pass


class ClientSocket(Socket):
    def start(self):
        self.socket.connect((self.host, self.port))

    def send(self, data):
        self.socket.send(json.dumps(data).encode('utf-8'))


class ServerSocket(Socket):
    @abstractmethod
    def process_requests(self):
        pass

    def start(self):
        self.socket.bind((self.host, self.port))
        self.socket.listen(1)


class WebServerSocket(ServerSocket):
    def __init__(self, host, port, web_server):
        super().__init__(host, port)
        self.web_server = web_server

    def process_requests(self):
        while True:
            client, address = self.socket.accept()
            print('Socket Accepted connection from: ', address)
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
