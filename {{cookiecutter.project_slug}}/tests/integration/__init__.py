import json
import re
import pkg_resources
import yaml
import unittest
from .. import client


class AbstractTest(unittest.TestCase):

    def setUp(self):
        apiFile = pkg_resources.resource_stream('{{cookiecutter.project_slug}}', 'schema/swagger.yml')
        self.url_prefix = yaml.load(apiFile)['basePath'][1:]

    def _prepare_url(self, url: str) -> str:
        if url[0] != '/':
            url = f"/{url}"
        return url

    def _get_status(self, status: str) -> int:
        # Status code contains strings: '200 OK'. Remove them
        return int(re.match(r"\d+", status).group(0))

    def post_json(self, url: str, data: dict):
        url = self._prepare_url(url)
        response = client.post(f"{self.url_prefix}{url}", data=json.dumps(data),
                               content_type='application/json',
                               follow_redirects=True)

        status_code = self._get_status(response.status)
        return json.loads(response.data), status_code

    def get_json(self, url: str):
        url = self._prepare_url(url)
        response = client.get(f"{self.url_prefix}{url}", follow_redirects=True)

        status_code = self._get_status(response.status)
        return json.loads(response.data), int(status_code)
