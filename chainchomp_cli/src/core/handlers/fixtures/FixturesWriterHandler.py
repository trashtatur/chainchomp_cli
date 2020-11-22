import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.data import PathProvider


class FixturesWriterHandler:

    DEFAULT_CONFIG_DICT = {
        'chainlink': {
            'name': 'default',
            'next': 'default',
        },
        'start': 'echo "no start script provided"',
        'stop': 'echo "no stop script provided"',
        'profile': 'default',
        'adapter': 'rabbitmq'
    }

    @staticmethod
    def write_default_chainfile_config():
        with open(os.path.join(PathProvider.fixtures_folder(), 'chainfile_default.yml'), 'w') as default_config:
            try:
                yaml.safe_dump(FixturesWriterHandler.DEFAULT_CONFIG_DICT, default_config, default_flow_style=False)
            except yaml.YAMLError as exception:
                LoggerInterface.error(f'Failed to dump information into default config file with exception: {exception}')
                return False
            else:
                return True
