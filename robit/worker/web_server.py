import json
from http.server import HTTPServer

from robit.core.web_server import WebServer, WebRequestHandler, html_encode_file, path_root_from_key


class WorkerWebServer(WebServer):
    def httpd_serve(self):
        api_json_data = self.api_json
        key = self.key
        path_root = path_root_from_key(key)

        class WorkerWebRequestHandler(WebRequestHandler):
            def do_GET(self):
                self._set_headers()

                if self.path == f'{path_root}/api/':
                    self.wfile.write(json.dumps(api_json_data, indent=4).encode("utf8"))

                elif self.served_css_js():
                    pass

                elif self.path == f'{path_root}/':
                    self.wfile.write(html_encode_file('worker_index.html'))

                else:
                    self.not_found()

        httpd = HTTPServer((self.address, self.port), WorkerWebRequestHandler)
        httpd.serve_forever()
