import json
from urllib import parse
from http.server import HTTPServer

from robit.core.web_server import WebServer, WebRequestHandler, html_encode_file, path_root_from_key


class MonitorWebServer(WebServer):
    def httpd_serve(self):
        api_json_data = self.api_json
        key = self.key
        path_root = path_root_from_key(key)

        class MonitorWebRequestHandler(WebRequestHandler):
            def do_GET(self):
                self._set_headers()

                print(self.path)

                if self.path == f'{path_root}/api/':
                    self.wfile.write(json.dumps(api_json_data, indent=4).encode("utf8"))

                elif self.path == f'{path_root}/worker_update/':
                    self.wfile.write('Try Posting to This Path'.encode("utf8"))

                elif self.served_css_js():
                    pass

                elif self.path == f'{path_root}/':
                    self.wfile.write(html_encode_file('monitor_index.html'))

                else:
                    self.not_found()

            # todo: Figure out how to decode complex dictionaries
            def do_POST(self):
                if self.path == f'{path_root}/worker_update/':
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    post_data_str = str(post_data)[2:-1]
                    print(post_data_str)
                    print(dict(parse.parse_qsl(post_data_str)))

        httpd = HTTPServer((self.address, self.port), MonitorWebRequestHandler)
        httpd.serve_forever()
