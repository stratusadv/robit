import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path

from robit.web_server.utils import html_encode_file


class WebRequestHandler(BaseHTTPRequestHandler):
    api_dict: dict
    key: str
    html_replace_dict: dict

    def not_found(self) -> None:
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
        if self.is_in_path_list([self.key, 'worker_api']):
            self._set_headers()
            worker_dict = {
                'id': self.api_dict['id'],
                'name': self.api_dict['name'],
                'groups': self.api_dict['groups'],
                'health': self.api_dict['health'],
                'clock': self.api_dict['clock'],
            }
            self.wfile.write(json.dumps(worker_dict, indent=4).encode("utf8"))

        elif self.is_in_path_list([self.key, 'job_api']):
            self._set_headers()
            if len(self.path_list) == 3:
                job_key = self.path_list[2]
            elif len(self.path_list) == 2:
                job_key = self.path_list[1]
            else:
                job_key = None

            if job_key:
                try:
                    job_dict = {
                        'job_detail': self.api_dict['job_details'][job_key]
                    }
                    self.wfile.write(json.dumps(job_dict, indent=4).encode("utf8"))
                except KeyError:
                    pass

        elif self.served_static():
            pass

        elif self.is_in_path_list([self.key]):
            self._set_headers()
            self.wfile.write(html_encode_file('worker.html', replace_dict=self.html_replace_dict))

        else:
            self._set_headers()
            self.not_found()

    def do_HEAD(self) -> None:
        self._set_headers()

    def do_POST(self) -> None:
        self._set_headers()
        self.not_found()


