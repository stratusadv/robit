import json
from pathlib import Path
from urllib.parse import quote_plus
from urllib.request import Request, urlopen


def get_text_from_file(name: str) -> str:
    return Path(Path(__file__).parent.parent.resolve(), 'html', name).read_text()


def html_encode_file(name: str, replace_dict: dict = None) -> bytes:
    html = get_text_from_file(name)

    if replace_dict:
        html_str = str(html)

        for key, val in replace_dict.items():
            html_str = html_str.replace(f'||{key}||', val)

        return html_str.encode("utf8")

    else:
        return html.encode("utf8")


def post_worker_data_to_monitor(address: str, key: str, post_dict: dict) -> None:
    try:
        request = Request(f'{address}/{key}/worker_update/', quote_plus(json.dumps(post_dict)).encode())
        urlopen(request)
    except:
        pass
