import os

import yaml
from chainchomplib import LoggerInterface
from chainchomplib.abstracts.AbstractResolver import AbstractResolver
from chainchomplib.configlayer.model.ChainfileModel import ChainfileModel
from chainchomplib.configlayer.resolver.ChainfileResolver import ChainfileResolver
from chainchomplib.data import PathProvider


class ChainlinkResolver(AbstractResolver):

    @staticmethod
    def resolve(name: str) -> ChainfileModel or None:

        if not os.path.isfile(os.path.join(PathProvider.chainlinks_folder(), f'{name}.yml')):
            LoggerInterface.warning(f'A chainlink with the name {name} is not registered')
            return None

        with open(os.path.join(PathProvider.chainlinks_folder(), f'{name}.yml', 'r')) as registered_chainlink:
            try:
                data = yaml.safe_load(registered_chainlink)
            except yaml.YAMLError as exception:
                LoggerInterface.error(f'Chainlink file could not be loaded with exception: {exception}')
            else:
                location = data['path']
                return ChainfileResolver.resolve_config_file(location)
            finally:
                registered_chainlink.close()
