import os
import shutil
import unittest

import yaml
from chainchomplib.data import PathProvider

from chainchomp_cli.src.core.handlers.fixtures.FixturesWriterHandler import FixturesWriterHandler


class FixturesWriterHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.fixtures_path = PathProvider.fixtures_folder()
        self.DEFAULT_CONFIG_DICT = {
            'chainlink': {
                'name': 'default',
                'next': 'default',
            },
            'start': 'echo "no start script provided"',
            'stop': 'echo "no stop script provided"',
            'profile': 'default',
            'adapter': 'rabbitmq'
        }
        os.mkdir(PathProvider.fixtures_folder())

    def tearDown(self) -> None:
        try:
            shutil.rmtree(PathProvider.fixtures_folder())
        except OSError:
            pass

    def test_that_default_config_fixture_gets_created(self):
        result = FixturesWriterHandler.write_default_chainfile_config()
        assert result is True

    def test_that_default_config_fixture_is_correct(self):
        FixturesWriterHandler.write_default_chainfile_config()
        with open(os.path.join(self.fixtures_path, 'chainfile_default.yml')) as created_file:
            created_config = yaml.safe_load(created_file)
            assert created_config == self.DEFAULT_CONFIG_DICT


if __name__ == '__main__':
    unittest.main()
