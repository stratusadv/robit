import os
from time import sleep

web_dir = os.path.join(os.path.dirname(__file__), 'robit/web')
os.chdir(web_dir)

from robit import Robit
from urllib import parse
import json
from pathlib import Path

import threading

rb = Robit('Epiphany Real Estate Finder')


if __name__ == '__main__':

    memory_value = 0

    from http.server import HTTPServer, BaseHTTPRequestHandler
    import socketserver

    PORT = 8000

    class S(BaseHTTPRequestHandler):
        def _set_headers(self):
            self.send_response(200)
            self.send_header("Content-type", "text/html")
            self.end_headers()

        def do_GET(self):

            def encode_file(name):
                html = Path(Path().resolve(), name).read_text()
                return html.encode("utf8")

            self._set_headers()
            if self.path == '/api':
                a_dict = {
                    'Hello World': memory_value,
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
                html = Path(Path().resolve(), 'index.html').read_text()
                self.wfile.write(html.encode("utf8"))

        def do_HEAD(self):
            self._set_headers()

        def do_POST(self):
            # Doesn't do anything with posted data
            self._set_headers()
            self.wfile.write('nothing to see here'.encode("utf8"))


    def run(server_class=HTTPServer, handler_class=S, addr="localhost", port=8000):
        server_address = (addr, port)
        httpd = server_class(server_address, handler_class)

        print(f"Starting httpd server on {addr}:{port}")
        httpd.serve_forever()

    thread = threading.Thread(target = run)
    thread.daemon = True
    thread.start()

    for i in range(20):
        print(i)
        memory_value = i
        sleep(1)