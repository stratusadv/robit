from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
import threading


class WebServer:
    def __init__(self):
        self.api_json = dict()
        self.web_server_thread = threading.Thread(target=self.httpd_serve)
        self.web_server_thread.daemon = True

    def httpd_serve(self, address="localhost", port=8000):

        web_json_data = self.api_json

        class WebRequestHandler(BaseHTTPRequestHandler):
            def _set_headers(self):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()

            def do_GET(self):
                def encode_file(name):
                    html = Path(Path().resolve(), 'robit/web', name).read_text()
                    return html.encode("utf8")

                self._set_headers()

                if self.path == '/api':
                    self.wfile.write(json.dumps(web_json_data, indent=4).encode("utf8"))
                elif 1 < len(self.path.split('.')) < 3:
                    if self.path[1:].split('.')[1] in ('js', 'css', 'html'):
                        self.wfile.write(encode_file(self.path[1:]))
                else:
                    self.wfile.write(encode_file('index.html'))

            def do_HEAD(self):
                self._set_headers()

            def do_POST(self):
                self._set_headers()
                self.wfile.write('Nothing to See Here'.encode("utf8"))

        httpd = HTTPServer((address, port), WebRequestHandler)

        print(f"Starting httpd server on {address}:{port}")
        httpd.serve_forever()

    def restart(self):
        pass

    def start(self):
        self.web_server_thread.start()

    def stop(self):
        pass

    def update_api_dict(self, update_dict: dict):
        for key, val in update_dict.items():
            self.api_json[key] = val
