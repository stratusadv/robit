from http.server import HTTPServer, BaseHTTPRequestHandler
import json
from pathlib import Path
from time import sleep

import threading


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
            a_dict = {
                'Hello World': 'Something',
            }
            a_json = json.dumps(a_dict, indent=4)
            self.wfile.write(a_json.encode("utf8"))
        elif self.path == '/index.js':
            self.wfile.write(encode_file('index.js'))
        elif self.path == '/index.css':
            self.wfile.write(encode_file('index.css'))
        elif self.path == '/bootstrap.bundle.min.js':
            self.wfile.write(encode_file('bootstrap.bundle.min.js'))
        elif self.path == '/bootstrap.min.css':
            self.wfile.write(encode_file('bootstrap.min.css'))
        else:
            self.wfile.write(encode_file('index.html'))

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        # Doesn't do anything with posted data
        self._set_headers()
        self.wfile.write('nothing to see here'.encode("utf8"))


class WebServer:
    def __init__(self):
        self.memory_value = 0
        thread = threading.Thread(target=self.httpd_serve)
        thread.daemon = True
        thread.start()

    def httpd_serve(self, address="localhost", port=8000):
        httpd = HTTPServer((address, port), WebRequestHandler)

        print(f"Starting httpd server on {address}:{port}")
        httpd.serve_forever()


