import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.abstracts.AbstractResolver import AbstractResolver
from chainchomplib.data import PathProvider


class AdapterResolver(AbstractResolver):

    @staticmethod
    def resolve(name: str) -> dict or None:

        if not os.path.isfile(os.path.join(PathProvider.installed_adapters_folder(), f'{name}.yml')):
            LoggerInterface.warning(f'An adapter with the name {name} is not registered')
            return None

        with open(os.path.join(PathProvider.installed_adapters_folder(), f'{name}.yml', 'r')) as registered_adapter:
            try:
                data = yaml.safe_load(registered_adapter)
            except yaml.YAMLError as exception:
                LoggerInterface.error(f'Adapter file could not be loaded with exception: {exception}')
            else:
                return data
            finally:
                registered_adapter.close()
