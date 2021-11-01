from http.server import BaseHTTPRequestHandler
from pathlib import Path
import threading


def html_encode_file(name, directory: str = 'robit/html', replace_dict: dict = None):
    html = Path(Path().resolve(), directory, name).read_text()

    if replace_dict:
        html_str = str(html)

        for key, val in replace_dict.items():
            html_str = html_str.replace(key, val)

        return html_str.encode("utf8")

    else:
        return html.encode("utf8")


def path_root_from_key(key):
    if key:
        return f'/{key}'
    else:
        return ''


class WebRequestHandler(BaseHTTPRequestHandler):
    def not_found(self):
        self.wfile.write('Nothing to See Here'.encode("utf8"))

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
    def __init__(self, address='localhost', port=8000, key=None):
        self.api_json = dict()
        self.post_dict = dict()

        self.address = address
        self.port = port
        self.key = key

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

        print(f'Starting httpd server an {href_link}')

    def stop(self):
        pass

    def update_api_dict(self, update_dict: dict):
        for key, val in update_dict.items():
            self.api_json[key] = val
