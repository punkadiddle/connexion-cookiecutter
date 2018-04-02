import unittest
import pkg_resources
from prance import ResolvingParser


class TestSpec(unittest.TestCase):

    def test_api_spec(self):
        apiFile = pkg_resources.resource_filename('{{cookiecutter.project_slug}}', 'schema/swagger.yml')
        self.assertTrue(apiFile.endswith('app_v1.yml'))
        parser = ResolvingParser(apiFile)
        self.assertIsNotNone(parser)


if __name__ == '__main__':
    unittest.main()
