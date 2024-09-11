import threading
from typing import Optional
from http.server import HTTPServer

from robit.web_server.request_handler import WebRequestHandler


class WebServer:
    def __init__(
            self,
            address: str = 'localhost',
            port: int = 8000,
            key: Optional[str] = None,
            html_replace_dict: Optional[dict] = None
    ) -> None:
        self.api_dict = dict()
        self.post_dict = dict()

        self.address = address
        self.port = port
        self.key = key


        self.worker_conn = None

        self.html_replace_dict = html_replace_dict

    def httpd_serve(self):
        WebRequestHandler.api_dict = self.api_dict
        WebRequestHandler.key = self.key
        WebRequestHandler.html_replace_dict = self.html_replace_dict
        WebRequestHandler.worker_conn = self.worker_conn

        httpd = HTTPServer((self.address, self.port), WebRequestHandler)
        httpd.serve_forever()

    def restart(self) -> None:
        pass

    def start(self) -> None:
        threading.Thread(target=self.httpd_serve).start()
        threading.Thread(target=self.update_api_dict).start()

        href_link = f'http://{self.address}:{self.port}'
        if self.key:
            href_link += f'/{self.key}/'

        print(f'Starting httpd server at {href_link}')

        if self.key is None:
            print(f'We do not recommend running servers with out keys!')

    def stop(self) -> None:
        pass

    def update_api_dict(self) -> None:
        while True:
            if self.worker_conn.poll():
                update_dict = self.worker_conn.recv()
                for key, val in update_dict.items():
                    self.api_dict[key] = val
