import ast
import json
import urllib.parse
from http.server import HTTPServer

from robit.web_server.web_server import WebServer, WebRequestHandler
from robit.web_server.utils import html_encode_file


class MonitorWebServer(WebServer):
    def httpd_serve(self):
        api_dict = self.api_dict
        post_dict = self.post_dict
        key = self.key
        html_replace_dict = self.html_replace_dict

        class MonitorWebRequestHandler(WebRequestHandler):
            def do_GET(self):

                if self.is_in_path_list([key, 'monitor_api']):
                    self._set_headers()
                    self.wfile.write(json.dumps(api_dict, indent=4).encode("utf8"))

                elif self.served_static():
                    pass

                elif self.is_in_path_list([key]):
                    self._set_headers()
                    self.wfile.write(html_encode_file('monitor.html', replace_dict=html_replace_dict))

                else:
                    self._set_headers()
                    self.not_found()

            def do_POST(self):
                if self.is_in_path_list([key, 'worker_update']):
                    content_length = int(self.headers['Content-Length'])
                    post_data = self.rfile.read(content_length)
                    post_data_dict = ast.literal_eval(urllib.parse.unquote_plus(str(post_data)[2:-1]))
                    post_dict['worker_dict'][post_data_dict['id']] = post_data_dict
                    # print(f'{post_dict = }')

        httpd = HTTPServer((self.address, self.port), MonitorWebRequestHandler)
        httpd.serve_forever()
