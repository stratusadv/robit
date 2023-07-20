from typing import Optional
from http.server import BaseHTTPRequestHandler
from pathlib import Path
import threading

from robit.socket.socket import WebServerSocket
from robit.web_server.utils import html_encode_file


class WebRequestHandler(BaseHTTPRequestHandler):
    def not_found(self):
        self.wfile.write('Nothing to See Here'.encode("utf8"))

    @property
    def path_list(self) -> list:
        temp_path_list = self.path.split('/')
        path_list = list()

        for path in temp_path_list:
            if len(path) > 0:
                path_list.append(path)

        return path_list

    def is_in_path_list(self, path_list: list) -> bool:
        if len(path_list) >= 1:
            if path_list[0] is None:
                del path_list[0]

        if len(path_list) <= len(self.path_list):
            for i in range(len(path_list)):
                if path_list[i] != self.path_list[i]:
                    return False
            else:
                return True
        else:
            return False

    def served_static(self) -> bool:
        if 1 < len(self.path.split('.')) < 3:
            extension = self.path[1:].split('.')[1]
            if extension in ('js', 'css', 'html', 'png'):
                if len(self.path.split('/')) > 2:
                    file_name = self.path.split('/')[2]
                else:
                    file_name = self.path[1:]

                if extension == 'png':
                    self._set_headers('png')
                    file_path = Path(Path(__file__).parent.parent.resolve(), 'html', file_name)
                    with open(file_path, "rb") as imageFile:
                        self.wfile.write(imageFile.read())
                else:
                    self._set_headers()
                    self.wfile.write(html_encode_file(file_name))

                return True

        return False

    def _set_headers(self, content_type: str = 'text/html') -> None:
        self.send_response(200)
        self.send_header("Content-type", content_type)
        self.end_headers()

    def do_GET(self):
        pass

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.not_found()


class WebServer:
    def __init__(
            self,
            address: str = 'localhost',
            port: int = 8000,
            key: Optional[str] = None,
            html_replace_dict: Optional[dict] = None
    ):
        self.api_dict = dict()
        self.post_dict = dict()

        self.address = address
        self.port = port
        self.key = key

        self.html_replace_dict = html_replace_dict

    def httpd_serve(self):
        pass

    def restart(self):
        pass

    def start_socket(self):
        socket = WebServerSocket(
            host='localhost',
            port=8000,
            web_server=self
        )
        socket.start()
        socket.process_requests()

    def start(self):
        threading.Thread(target=self.httpd_serve).start()
        threading.Thread(target=self.start_socket).start()

        href_link = f'http://{self.address}:{self.port}'
        if self.key:
            href_link += f'/{self.key}/'

        print(f'Starting httpd server at {href_link}')

        if self.key is None:
            print(f'We do not recommend running servers with out keys!')

    def stop(self):
        pass

    def update_api_dict(self, update_dict: dict):
        for key, val in update_dict.items():
            self.api_dict[key] = val
