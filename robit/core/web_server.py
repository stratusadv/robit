from http.server import BaseHTTPRequestHandler
from pathlib import Path
import threading


def html_encode_file(name, directory: str = 'html', replace_dict: dict = None):
    html = Path(Path(__file__).parent.parent.resolve(), directory, name).read_text()

    if replace_dict:
        html_str = str(html)

        for key, val in replace_dict.items():
            html_str = html_str.replace(f'||{key}||', val)

        return html_str.encode("utf8")

    else:
        return html.encode("utf8")


class WebRequestHandler(BaseHTTPRequestHandler):
    def not_found(self):
        self.wfile.write('Nothing to See Here'.encode("utf8"))

    @property
    def path_list(self):
        temp_path_list = self.path.split('/')
        path_list = list()

        for path in temp_path_list:
            if len(path) > 0:
                path_list.append(path)

        return path_list

    def is_in_path_list(self, path_list: list):
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

    def served_css_js(self):
        if 1 < len(self.path.split('.')) < 3:
            if self.path[1:].split('.')[1] in ('js', 'css', 'html'):
                if len(self.path.split('/')) > 2:
                    file_name = self.path.split('/')[2]
                else:
                    file_name = self.path[1:]

                self.wfile.write(html_encode_file(file_name))

                return True

        return False

    def _set_headers(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        pass

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        self._set_headers()
        self.not_found()


class WebServer:
    def __init__(self, address='localhost', port=8000, key=None, html_replace_dict=None):
        self.api_dict = dict()
        self.post_dict = dict()

        self.address = address
        self.port = int(port)
        self.key = key

        self.html_replace_dict = html_replace_dict

        self.thread = threading.Thread(target=self.httpd_serve)
        self.thread.daemon = True

    # Override this Function to customize the webserver
    def httpd_serve(self):
        pass

    def restart(self):
        pass

    def start(self):
        self.thread.start()
        href_link = f'http://{self.address}:{self.port}'

        if self.key:
            href_link += f'/{self.key}/'

        print(f'Starting httpd server at {href_link}')

    def stop(self):
        pass

    def update_api_dict(self, update_dict: dict):
        for key, val in update_dict.items():
            self.api_dict[key] = val
