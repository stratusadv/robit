import json
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


def post_worker_data_to_monitor(address, key, post_dict):
    try:
        request = Request(f'{address}/{key}/worker_update/', quote_plus(json.dumps(post_dict)).encode())
        urlopen(request)
    except:
        pass