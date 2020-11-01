import os
import unittest

from chainchomplib.configlayer.model.ChainlinkConfigModel import ChainlinkConfigModel
from chainchomplib.data import PathProvider
from parameterized import parameterized

from chainchomp_cli.src.core.handlers.config_file.ConfigReadHandler import ConfigReadHandler


class ConfigReadHandlerTest(unittest.TestCase):

    def setUp(self) -> None:
        self.configPath = os.path.join(PathProvider.base_config_folder(), 'configFileReader')
        self.chainlinkConfigModel = ChainlinkConfigModel(
            'test project',
            'test name',
            'test next',
            'test previous',
            'test start',
            'test stop',
            True,
            'test adapter',
            'test profile'
        )

    @parameterized.expand([
        ('chainfile', None),
        ('faultyConfigFile.yml', None),
        ('thisDoesNotExists', None),
        ('thisDoesNotExists.yml', None)
    ])
    def test_that_no_wrong_name_works(self, path, expected):
        result = ConfigReadHandler.read_config_file(os.path.join(self.configPath, 'wrong_name', path))
        assert result is expected

    @parameterized.expand([
        ('base_folder_supplied', True),
        ('chainfile.yml', True)
    ])
    def test_that_file_can_be_found_in_path(self, path: str, expected: bool):
        result = ConfigReadHandler.read_config_file(os.path.join(self.configPath, path))
        assert isinstance(result, ChainlinkConfigModel) is expected

    def test_that_model_gets_created_correctly(self):
        result = ConfigReadHandler.read_config_file(os.path.join(self.configPath, 'chainfile.yml'))
        assert result == self.chainlinkConfigModel


if __name__ == '__main__':
    unittest.main()
