import json
from http.server import HTTPServer

from robit.core.web_server import WebServer, WebRequestHandler, html_encode_file


class WorkerWebServer(WebServer):
    def httpd_serve(self):
        api_dict = self.api_dict
        key = self.key
        html_replace_dict = self.html_replace_dict

        class WorkerWebRequestHandler(WebRequestHandler):
            def do_GET(self):

                if self.is_in_path_list([key, 'worker_api']):
                    self._set_headers()
                    worker_dict = {
                        'id': api_dict['id'],
                        'name': api_dict['name'],
                        'groups': api_dict['groups'],
                        'health': api_dict['health'],
                        'status': api_dict['status'],
                        'clock': api_dict['clock'],
                    }
                    self.wfile.write(json.dumps(worker_dict, indent=4).encode("utf8"))

                elif self.is_in_path_list([key, 'job_api']):
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
                                'job_detail': api_dict['job_details'][job_key]
                            }
                            self.wfile.write(json.dumps(job_dict, indent=4).encode("utf8"))
                        except KeyError:
                            pass

                elif self.served_static():
                    pass

                elif self.is_in_path_list([key]):
                    self._set_headers()
                    self.wfile.write(html_encode_file('worker.html', replace_dict=html_replace_dict))

                else:
                    self._set_headers()
                    self.not_found()

        httpd = HTTPServer((self.address, self.port), WorkerWebRequestHandler)
        httpd.serve_forever()
