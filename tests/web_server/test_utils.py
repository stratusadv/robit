import unittest

from robit.web_server import utils


class TestUtils(unittest.TestCase):
    def test_html_encode_file(self):
        html = utils.html_encode_file('worker.html')
        self.assertTrue(html[1:5] == b'html')

        html = utils.html_encode_file('worker.html', {'title': 'hello world'})
        self.assertTrue(b'hello world' in html)
