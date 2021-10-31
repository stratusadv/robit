from urllib.parse import urlencode
from urllib.request import Request, urlopen


# todo: Figure out how to encode complex dictionaries
def post_worker_data_to_monitor(address, key, post_dict):
    try:
        request = Request(f'{address}/{key}/worker_update/', urlencode(post_dict).encode())
        print(f'{address}/{key}/worker_update/')
        urlopen(request)
    except:
        pass