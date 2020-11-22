import os
import shutil
import unittest

import yaml
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.data import PathProvider
from parameterized import parameterized

from chainchomp_cli.src.core.handlers.config_file.ConfigWriterHandler import ConfigWriterHandler


class ConfigWriterHandlerTest(unittest.TestCase):

    def setUp(self, fs=None) -> None:
        self.configPath = os.path.join(PathProvider.base_config_folder(), 'configFileWriter')
        os.mkdir(self.configPath)
        self.chainlinkModel = ChainfileModel(
            'test',
            'test',
            'test',
            'test',
            'test',
            'test',
            'test',
            'test'
        )
        self.chainlink_dict = {
            'project': 'test',
            'chainlink': {
                'name': 'test',
                'next': 'test',
                'previous': 'test',
            },
            'start': 'test',
            'stop': 'test',
            'profile': 'test'
        }

    def tearDown(self) -> None:
        shutil.rmtree(self.configPath)

    def test_writing_successful(self):
        ConfigWriterHandler.write_config_file(self.chainlinkModel, self.configPath, False)
        with open(os.path.join(self.configPath, 'chainfile.yml')) as testfile:
            test_written_dict = yaml.safe_load(testfile)
            assert test_written_dict == self.chainlink_dict

    @parameterized.expand([
        (os.path.join(PathProvider.env_based_base_folder(), 'chainchomp'), False),
        (os.path.join(PathProvider.env_based_base_folder(), 'chainlink'), False)
    ])
    def test_path_does_not_exist(self, path, expected):
        result = ConfigWriterHandler.write_config_file(self.chainlinkModel, path, False)
        assert expected == result

    def test_file_already_exists(self):
        open(os.path.join(self.configPath, 'chainfile.yml'), 'x')
        result = ConfigWriterHandler.write_config_file(self.chainlinkModel, self.configPath, False)
        assert result is None

    def test_file_is_overwritten_on_force(self):
        open(os.path.join(self.configPath, 'chainfile.yml'), 'x')
        result = ConfigWriterHandler.write_config_file(self.chainlinkModel, self.configPath, True)
        assert result is True


if __name__ == '__main__':
    unittest.main()
