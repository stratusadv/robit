import ast
import json
import urllib.parse
from urllib import parse
from http.server import HTTPServer

from robit.core.web_server import WebServer, WebRequestHandler, html_encode_file


class MonitorWebServer(WebServer):
    def httpd_serve(self):
        api_dict = self.api_dict
        post_dict = self.post_dict
        key = self.key
        html_replace_dict = self.html_replace_dict

        class MonitorWebRequestHandler(WebRequestHandler):
            def do_GET(self):
                self._set_headers()

                if self.is_in_path_list([key, 'monitor_api']):
                    self.wfile.write(json.dumps(api_dict, indent=4).encode("utf8"))

                elif self.served_css_js():
                    pass

                elif self.is_in_path_list([key]):
                    self.wfile.write(html_encode_file('monitor_index.html', replace_dict=html_replace_dict))

                else:
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
